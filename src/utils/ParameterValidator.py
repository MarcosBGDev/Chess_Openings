import datetime

class ParameterValidator:

    @staticmethod
    def ask_parameters() -> tuple[int, int, int]:
        while True:
            try:
                n_top = int(input("Introduce el número de jugadores top (1-50): "))
                n_top = ParameterValidator.validate_n_top(n_top)

                start_year = int(input("Introduce el año de inicio (>= 2008): "))
                start_year = ParameterValidator.validate_start_year(start_year)

                end_year = int(input("Introduce el año final (<= año actual): "))
                end_year = ParameterValidator.validate_end_year(end_year)

                ParameterValidator.validate_year_range(start_year, end_year)

                return n_top, start_year, end_year

            except ValueError as e:
                print(f"Error: {e}\nPor favor, inténtalo de nuevo.\n")

    @staticmethod
    def validate_n_top(n_top: int) -> int:
        ParameterValidator.ensure_int(n_top, "El número de jugadores")
        if n_top <= 0:
            raise ValueError("El número de jugadores debe ser mayor que 0.")
        if n_top > 50:
            raise ValueError("El número de jugadores no puede ser mayor que 50.")
        return n_top

    @staticmethod
    def validate_start_year(start_year: int, min_year: int = 2008) -> int:
        """Comprueba que el año inicial no sea menor que el año mínimo permitido (por defecto 2008)."""
        ParameterValidator.ensure_int(start_year, "El año inicial")
        if start_year < min_year:
            raise ValueError(f"El año inicial no puede ser menor que {min_year}.")
        return start_year

    @staticmethod
    def get_current_year() -> int:
        """ Devuelve el año actual"""
        return datetime.datetime.now().year

    @staticmethod
    def validate_end_year(end_year: int) -> int:
        """ Comprueba que el año final no supere el año actual. Sería ineficiente de cara a obtener partidas"""
        ParameterValidator.ensure_int(end_year, "El año final")
        current_year = ParameterValidator.get_current_year()
        if end_year > current_year:
            raise ValueError(f"El año final no puede ser mayor que el año actual ({current_year}).")
        return end_year

    @staticmethod
    def validate_year_range(start_year: int, end_year: int):
        """ Comprueba que el año inicial no supere el final"""
        if start_year > end_year:
            raise ValueError("El año inicial no puede ser mayor que año final.")

    @staticmethod
    def ensure_int(value, name: str) -> int:
        """ Comprueba que el número que se le da sea de tipo entero """
        if not isinstance(value, int):
            raise ValueError(f"{name} debe ser un entero.")
        return value