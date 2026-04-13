import os
import random
import statistics
import typer
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Importujemy logikę biznesową przygotowaną w zadaniu 5
from ex5 import get_file_path, extract_measurements
from getAddressesByCode import getAddressesByCode
import logging

app = typer.Typer(help="CLI do obróbki danych o jakości powietrza z 2023 r. (Typer)")
logger = logging.getLogger('zad5') # Używamy już skonfigurowanego loggera z ex5.py
console = Console()

@app.callback()
def main(
    ctx: typer.Context,
    quantity: str = typer.Option(..., "--quantity", "-q", help="Mierzona wielkość (np. PM10, PM2.5, NO2)"),
    freq: str = typer.Option(..., "--freq", "-f", help="Częstotliwość (1g, 24g, 1m)"),
    start: datetime = typer.Option(..., "--start", "-s", formats=["%Y-%m-%d"], help="Początek przedziału (rrrr-mm-dd)"),
    end: datetime = typer.Option(..., "--end", "-e", formats=["%Y-%m-%d"], help="Koniec przedziału (rrrr-mm-dd)")
):
    """
    Konfiguracja parametrów globalnych wywoływana przed subkomendami.
    """
    if start > end:
        console.print("❌ [bold red]Błąd krytyczny:[/bold red] Data początkowa nie może być późniejsza niż data końcowa.")
        raise typer.Exit(code=1)
        
    try:
        csv_path = get_file_path(quantity, freq)
    except Exception as e:
        console.print(f"⚠️ [bold yellow]Ostrzeżenie:[/bold yellow] Błąd argumentu - {e}")
        raise typer.Exit(code=1)

    # Przechowanie stanu w kontekście, aby był dostępny dla podkomend
    ctx.obj = {
        "quantity": quantity,
        "freq": freq,
        "start": start,
        "end": end,
        "csv_path": csv_path
    }

@app.command("random-station")
def random_station(ctx: typer.Context):
    """Wypisz nazwę i adres losowej stacji mierzącej tę wielkość w danym czasie."""
    obj = ctx.obj
    station_codes, data_per_station = extract_measurements(obj["csv_path"], obj["start"], obj["end"])
    
    valid_codes = [code for code, vals in data_per_station.items() if vals]
    
    if not valid_codes:
        console.print("⚠️ [bold yellow]Ostrzeżenie:[/bold yellow] Brak dostępnych pomiarów dla zadanych parametrów (filtr zwrócił pustą listę).")
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
            title=f"🏫 [bold green]Losowa stacja: {name}[/bold green]",
            border_style="green",
            expand=False
        )
        console.print(panel)
    else:
        console.print(f"⚠️ [bold yellow]Ostrzeżenie:[/bold yellow] Znaleziono stacje, ale nie ma jej w pliku stacje.csv (Kod: {random_code})")

@app.command("stats")
def stats(
    ctx: typer.Context, 
    station: str = typer.Argument(..., help="Kod stacji (np. DsGlogWiStwo)")
):
    """Oblicz średnią i odchylenie standardowe dla danej stacji."""
    obj = ctx.obj
    station_codes, data_per_station = extract_measurements(obj["csv_path"], obj["start"], obj["end"])
    
    if station not in data_per_station:
        console.print(f"⚠️ [bold yellow]Ostrzeżenie:[/bold yellow] Częstotliwość lub wielkość nie jest wspierana przez stację '{station}'.")
        return
        
    vals = data_per_station[station]
    if not vals:
        console.print(f"⚠️ [bold yellow]Ostrzeżenie:[/bold yellow] Brak poprawnych pomiarów dla zadanych parametrów w czasie (Stacja: '{station}').")
        return
        
    mean = statistics.mean(vals)
    stdev = statistics.stdev(vals) if len(vals) > 1 else 0.0
    
    table = Table(
        title=f"📊 Statystyki pomiarów dla [bold yellow]{station}[/bold yellow]",
        show_header=True, 
        header_style="bold magenta",
        title_justify="left"
    )
    table.add_column("Parametr", style="cyan", justify="right")
    table.add_column("Wartość", style="green", justify="left")
    
    table.add_row("Wielkość", obj['quantity'])
    table.add_row("Zakres czasu", f"{obj['start'].strftime('%Y-%m-%d')}  ➡  {obj['end'].strftime('%Y-%m-%d')}")
    table.add_row("Liczba pomiarów", str(len(vals)))
    table.add_row("Średnia", f"{mean:.2f}")
    if len(vals) > 1:
        table.add_row("Odchylenie stand.", f"{stdev:.2f}")
    else:
        table.add_row("Odchylenie stand.", "[red]Brak (wymagane min. 2)[/red]")
        
    console.print(table)

if __name__ == "__main__":
    app()