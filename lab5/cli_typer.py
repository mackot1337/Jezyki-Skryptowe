import os
import random
import statistics
import typer
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from cli_helper import setup_logging, get_file_path, extract_measurements, extract_station_measurements
from getAddressesByCode import getAddressesByCode
from findAnomaly import findAnomaly

app = typer.Typer(help="CLI do obróbki danych o jakości powietrza (Typer)")
logger = setup_logging()
console = Console()

@app.callback()
def main(
    ctx: typer.Context,
    quantity: str = typer.Option(..., "--quantity", "-q", help="Mierzona wielkość (np. PM10, PM2.5, NO2)"),
    freq: str = typer.Option(..., "--freq", "-f", help="Częstotliwość (1g, 24g, 1m)"),
    start: datetime = typer.Option(..., "--start", "-s", formats=["%Y-%m-%d"], help="Początek przedziału (rrrr-mm-dd)"),
    end: datetime = typer.Option(..., "--end", "-e", formats=["%Y-%m-%d"], help="Koniec przedziału (rrrr-mm-dd)")
):
    if start > end:
        console.print("[bold red]ERROR:[/bold red] Data początkowa nie może być późniejsza niż data końcowa.")
        raise typer.Exit(code=1)
        
    try:
        csv_path = get_file_path(quantity, freq)
    except Exception as e:
        console.print(f"[bold yellow]WARNING:[/bold yellow] Błąd argumentu - {e}")
        raise typer.Exit(code=1)

    ctx.obj = {
        "quantity": quantity,
        "freq": freq,
        "start": start,
        "end": end,
        "csv_path": csv_path
    }

@app.command("random-station")
def random_station(ctx: typer.Context):
    obj = ctx.obj
    data_per_station = extract_measurements(obj["csv_path"], obj["start"], obj["end"])
    
    valid_codes = [code for code, vals in data_per_station.items() if vals]
    
    if not valid_codes:
        console.print("[bold yellow]WARNING:[/bold yellow] Brak dostępnych pomiarów dla zadanych parametrów.")
        return
        
    random_code = random.choice(valid_codes)
    stacje_path = os.path.join(os.path.dirname(__file__), 'stacje.csv')
    addr_list = getAddressesByCode(stacje_path, random_code)
    
    if addr_list:
        county, city, street, number, name = addr_list[0]
        adres = f"{street} {number}".strip() if street else 'Brak adresu'
        
        info = f"[bold cyan]Adres:[/bold cyan] {city}, {adres}\n" \
               f"[bold cyan]Kod stacji:[/bold cyan] {random_code}\n" \
               f"[bold cyan]Województwo:[/bold cyan] {county}"
        
        panel = Panel(
            info,
            title=f"[bold green]Losowa stacja: {name}[/bold green]",
            border_style="purple",
            expand=False
        )
        console.print(panel)
    else:
        console.print(f"[bold yellow]WARNING:[/bold yellow] Znaleziono stacje, ale nie ma jej w pliku stacje.csv (Kod: {random_code})")

@app.command("stats")
def stats(
    ctx: typer.Context, 
    station: str = typer.Argument(..., help="Kod stacji (np. DsGlogWiStwo)")
):
    obj = ctx.obj
    data_per_station = extract_measurements(obj["csv_path"], obj["start"], obj["end"])
    
    if station not in data_per_station:
        console.print(f"[bold yellow]WARNING:[/bold yellow] Częstotliwość lub wielkość nie jest logowana przez stację '{station}'.")
        return
        
    vals = data_per_station[station]
    if not vals:
        console.print(f"[bold yellow]WARNING:[/bold yellow] Brak poprawnych pomiarów dla zadanych parametrów w czasie (Stacja: '{station}').")
        return
        
    mean = statistics.mean(vals)
    stdev = statistics.stdev(vals) if len(vals) > 1 else 0.0

    table = Table(
        header_style="bold magenta",
        title_justify="center",
        border_style="blue"
    )
    table.add_column("Parametr", style="bold cyan", justify="right")
    table.add_column("Wartość", style="white", justify="left")
    
    table.add_row("Wielkość", obj['quantity'])
    table.add_row("Zakres czasu", f"{obj['start'].strftime('%Y-%m-%d')}  ➡  {obj['end'].strftime('%Y-%m-%d')}")
    table.add_row("Liczba pomiarów", str(len(vals)))
    table.add_row("Średnia", f"{mean:.2f}")

    if len(vals) > 1:
        table.add_row("Odchylenie stand.", f"{stdev:.2f}")
    else:
        table.add_row("Odchylenie stand.", "[red]Brak (wymagane min. 2)[/red]")

    panel = Panel(
        table,
        title=f"[bold green]Statystyki dla stacji: [bold yellow]{station}[/bold yellow][/bold green]",
        border_style="purple",
        expand=False
    )
        
    console.print(panel)


@app.command("anomaly")
def anomaly(
    ctx: typer.Context,
    station: str = typer.Argument(..., help="Kod stacji (np. DsGlogWiStwo)"),
    alarm_limit: float = typer.Option(500.0, "--alarm-limit", help="Próg alarmowy"),
    jump_limit: float = typer.Option(100.0, "--jump-limit", help="Próg nagłego skoku")
):
    obj = ctx.obj
    measurements = extract_station_measurements(obj["csv_path"], obj["start"], obj["end"], station)

    if not measurements:
        console.print(f"[bold yellow]WARNING:[/bold yellow] Brak danych dla stacji '{station}' w zadanym przedziale czasu.")
        return

    result = findAnomaly(measurements, alarmLimit=alarm_limit, jumpLimit=jump_limit)

    table = Table(header_style="bold magenta", border_style="blue")
    table.add_column("Parametr", style="bold cyan", justify="right")
    table.add_column("Wartość", style="white", justify="left")
    table.add_row("Stacja", station)
    table.add_row("Wielkość", obj["quantity"])
    table.add_row("Błędy czujnika", str(result["bledy_czujnika_ilosc"]))
    table.add_row("Liczba ostrzeżeń", str(len(result["wykryte_ostrzezenia"])))

    console.print(Panel(table, title="[bold green]Wynik analizy anomalii[/bold green]", border_style="purple", expand=False))

    if result["wykryte_ostrzezenia"]:
        console.print("[bold yellow]Wykryte ostrzeżenia:[/bold yellow]")
        for item in result["wykryte_ostrzezenia"]:
            console.print(f"- {item}")
    else:
        console.print("[green]Brak anomalii.[/green]")

if __name__ == "__main__":
    app()