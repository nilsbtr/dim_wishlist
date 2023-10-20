import time

import dictonary_handler as dic
import manifest_update as update
import wishlist_utility as util
import wishlist_writer as writer
from config import Colors, Files, Tags


def main():
    print(f'{Tags.HEAD} Updating database and dictionary.')
    update.main()

    print(f'{Tags.HEAD} Loading dictionaries into memory.')
    dic.load()

    print(f'{Tags.HEAD} Start conversion of the wishlist.')
    start = time.time()

    writer.main()

    end = time.time()

    print(
        f'{Tags.HEAD} {Colors.GREEN}File successfully converted!{Colors.END} {writer.len_source()}/{dic.len_weapons()} possible Weapons found.'
    )
    print(
        f'{Colors.BLACK}Conversion performed in {Colors.PURPLE}{round(end - start, 5)}{Colors.END} {Colors.BLACK}seconds.{Colors.END}'
    )

    dic.out_errors()


if __name__ == "__main__":
    main()
