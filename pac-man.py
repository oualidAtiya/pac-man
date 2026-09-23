from src.config.loader import Loader


def main():
    loader = Loader()
    game_config = loader.load_config()
    print(game_config)
    


if __name__ == '__main__':
    main()