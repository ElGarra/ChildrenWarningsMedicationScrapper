"""Module to call main function"""
from scrapper import Scrapper

def main():
    """Main function"""
    scrapper = Scrapper()
    scrapper.run_scrapper()
    scrapper.write_data()

if __name__ == "__main__":
    main()
