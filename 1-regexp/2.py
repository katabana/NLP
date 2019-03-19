import regex
import os

# internal - meaning inside the bill for parts of the bill
# or internal meaning inside of any bill?

# regulation id?


# don't count references like this:

# W ustawie z dnia 30 czerwca 1970 r. o Inspekcji Skupu i Przetwórstwa Artykułów
# Rolnych (Dz.U. z 2000 r. Nr 23, poz. 293 i Nr 89, poz. 991) w art. 3 w ust. 1 w
# pkt 1 dodaje się lit. e)  w brzmieniu:
#      " e) domów składowych,".


# TODO: solve problem
# po ust. 2
# dodaje się ust. 2a w brzmieniu:

# TODO: MAKE RANKING FOR EVERY BILL


def find_references(filepath):
    print(filepath)

    with open(filepath, 'r') as bill_file:
        bill = bill_file.read()
        bill = regex.sub(r'[\t\p{Zs}\xA0\n]+', ' ', bill)  # remove redundant spaces

        # get sentences
        sentences = regex.findall(
            r"(?P<sent>(?:^|\.|\p{Lu})[\t\p{Zs}\xA0\n]*"
            r"\X*?"
            r"(?=(?:\.[\t\p{Zs}\xA0\n]*(?!U\.|Nr)(?:\p{Lu}|$)))"
            r")",
            bill)
            # 'Po ust. 2 dodaje się ust. 2a w brzmieniu:')

        # print(sentences)
        # exit(0)

        # TODO: find fragments starting with 'Art. X'

        parts = []
        # find the fragments with these references
        for sentence in sentences:
            part = regex.findall(
                r"(?:^|\.)"
                r"(?P<senten>(?!r\.|poz.)\X*?"
                r"(?P<ref>(?:art\.|ust\.)\X*)+"
                r"(?P<rest>(?:,)\X*)"
                r")",
                sentence
            )
            for record in part:
                # print(record[1])
                parts.append(record[1])

        references = []
        for fragment in parts:
            print("FRAG", fragment)

            test_sentence = 'Art. 2. Bart. 1, art. 200a, 20bb. W art. 100-103 ust. 300, 200 i 10 byyyy,' \
                            ' art. 400, 20. W art. 23 i 40, art. 30.' \
                            ' Art. 3. W art. 500, 502-505 i 60, bo ust. 70-78. W art. 90 i 91, art. 100.'
            # art. X (, X i X)

            # matches properly, saves if ust if it follows
            # finds both if art. (X) ust. (X)
            art = regex.findall(
                r"(?P<art>\bart\."
                # r"(?:(?P<big>\bArt\.\s\d+(?:\p{L}|))\X*?)?(?P<art>\bart\."
                r"(?:"
                r"(?:,\s|\s|\si\s)"
                r"\d+(?:\p{L}*|)"
                r")+"
                # r"(?=,\s\p{L}|\.|$|:)(?<!art\.)"
                r")"
                r"(?:\s(?P<ust>\bust\."
                r"(?:"
                r"(?:,\s|\s|\si\s)"
                r"\d+(?:\p{L}*|)"
                r")+)"
                # r"(?=,\s\p{L}|\.|$|:)(?<!art\.)"
                r")*"
                r"",
                test_sentence
                # fragment
            )

            art = regex.findall(
                r"(?P<art>\bart\."
                # r"(?:(?P<big>\bArt\.\s\d+(?:\p{L}|))\X*?)?(?P<art>\bart\."
                r"(?:"
                r"(?:,\s|\s|\si\s|-)"
                r"\d+(?:\p{L}*|)"
                r")+"
                # r"(?=,\s\p{L}|\.|$|:)(?<!art\.)"
                r")"
                r"(?:\s(?P<ust>\bust\."
                r"(?:"
                r"(?:,\s|\s|\si\s|-)"
                r"\d+(?:\p{L}*|)"
                r")+)"
                # r"(?=,\s\p{L}|\.|$|:)(?<!art\.)"
                r")*"
                r"",
                test_sentence
                # fragment
            )

            print("ART", art)
            # exit(0)

            # matches ust., if art. preceeds, then it is matched
            ust = regex.findall(
                # r"(?P<art>\bart\."
                r"(?:(?P<big>\bArt\.\s\d+(?:\p{L}|))\X*?)?(?P<art>\bart\."
                r"(?:"
                r"(?:,\s|\s|\si\s|-)"
                r"\d+(?:\p{L}*|)"
                r")+"
                r"\s)*"
                r"(?P<ust>\bust\."
                r"(?:"
                r"(?:,\s|\s|\si\s|-)"
                r"\d+(?:\p{L}*|)"
                r")+"
                # r"(?=,\s\p{L}|\.|$|:)(?<!art\.)"
                r")",
                test_sentence
                # fragment
            )

            # TODO: parse art. X, ust. X, art. X ust. X that were found
            # TODO: remember to do 'art. X ust. X' only once
            # TODO: problem -> how to get article of ust without art?

            # regulation ID

            print("ust", ust)
            # exit(0)

            exit(0)

            print('FRA', fragment)
            for ref in refs:
                if ref:
                    print("REF", ref)
                    references.append(ref)
        # print(references)
        exit(0)

    pass


def main():
    dir_path = 'ustawy'
    all_references = []

    n = 0
    for filename in os.listdir(dir_path):
        if n < 2000:
            all_references.append(find_references('{}/{}'.format(dir_path, filename)))
        n = n + 1

    # for testing:
    # filename = '2001_1188.txt'
    # all_references.append(find_references('{}/{}'.format(dir_path, filename)))

    # print("*** RANKING ***")
    # aggregated = aggregate_rankings(all_references)
    # print_ranking(aggregated)

main()
