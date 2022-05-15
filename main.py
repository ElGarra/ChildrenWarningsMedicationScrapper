from scrapper import Scrapper
from pprint import pprint
def main():

    scrapper = Scrapper()
    scrapper.runScrapper()
    # print(f"----------------------------------------LETTER {scrapper.alphabet[scrapper.run_letter_counter]}----------------------------------------")
    # for letra in scrapper.all_data:
    #     scrapper.run_letter_counter += 1
    #     if scrapper.run_letter_counter < len(scrapper.all_data):
    #         if letra == []:
    #             print("No available medications for letter: " + scrapper.alphabet[scrapper.run_letter_counter - 1])
    #         print(letra)
    #         print(f"\n----------------------------------------LETTER {scrapper.alphabet[scrapper.run_letter_counter]}----------------------------------------")
    # pprint(scrapper.all_data[-1])
    # print("----------------------------------------------------------")

    
    # pprint(scrapper.all_data)
    scrapper.writeData()
if __name__ == "__main__":
    main()