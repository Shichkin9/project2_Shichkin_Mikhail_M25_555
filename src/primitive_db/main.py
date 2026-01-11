#!/usr/bin/env python3

"""Входим в приложение (точка входа)"""

from .engine import DatabaseEngine


def main():
    """Основная функция нашего приложения."""
    engine = DatabaseEngine()
    engine.run()


if __name__ == "__main__":
    main()
