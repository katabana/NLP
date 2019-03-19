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


# TODO: case to consider:
# 8) w art. 8:
# a) ust. 1
# otrzymuje brzmienie:
# (...)
# b) w ust. 1a:
# – pkt 2 i 3


def make_range(article):
    arts_range = []
    match = regex.findall(r'(?P<sn>\d*)(?P<sl>\p{L}*)-(?P<en>\d*)(?P<el>\p{L}*)', article)
    sn, sl, en, el = match[0]
    for i in range(int(sn), int(en) + 1):
        if sl and el:
            for j in range(ord(sl), ord(el) + 1):
                arts_range.append(str(i)+chr(j))
        else:
            arts_range.append(str(i))
    return arts_range


def parse_prefix_numbers(prefix, art_text):
    final_articles = []
    art_text = regex.sub(prefix, '', art_text)
    art_text = regex.sub('\s(?:i|oraz)\s', ', ', art_text)
    articles = regex.split(', ', art_text)
    for article in articles:
        if '-' in article:
            final_articles += make_range(article)
        else:
            final_articles.append(article)

    return final_articles


def parse_articles_only(articles):
    references = {}
    for art, ust in articles:
        # for art. X only
        arts = parse_prefix_numbers(r'art\. ', art)
        if not ust:
            for a in arts:
                id = 'art. ' + a
                if id in references:
                    n = references[id]
                    references[id] = n + 1
                else:
                    references[id] = 1
    return references


def parse_paragraphs(paragraphs):
    references = {}
    last_art = ''
    for art_ref, art, par in paragraphs:
        if art_ref:
            last_art = parse_prefix_numbers(r'art\. ', art_ref)[-1]
        article = 'art. ' + parse_prefix_numbers(r'art\. ', art)[-1]
        pars = parse_prefix_numbers(r'ust\. ', par)
        if not art:
            article = regex.sub(r'A', 'a', last_art)

        id = article
        if id:
            id = id + ', '
        for p in pars:
            p_id = id + 'ust. ' + p
            if p_id in references:
                n = references[p_id]
                references[p_id] = n + 1
            else:
                references[p_id] = 1
    return references


def merge_references(rankings):
    final = {}
    for ranking in rankings:
        for id, value in ranking.items():
            if id in final:
                last_value = final[id]
                final[id] = last_value + value
            else:
                final[id] = value
    return final


def find_references(filepath):
    print(filepath)

    with open(filepath, 'r') as bill_file:
        bill = bill_file.read()
        bill = regex.sub(r'[\t\p{Zs}\xA0\n]+', ' ', bill)  # remove redundant spaces

        # PROBLEM: with citations -> it is not that simple -> how to distinguish which " should end the citation?
        # there are internal "" as well.

        # remove citations
        # test_citation = 'AAAAadsd „bbbbbb” "Cccc"  ajjasjdsahs'
        # bill = regex.sub(r'(?:„\X*?”|"\X*?")', '', bill)

        # Articles may be 'Art. D+L*'

        # find fragments starting with 'Art. X' (until next Art or $?)
        sentences = regex.findall(
            r"(?P<sent>(?:^|)Art\."
            r"\X*?)(?=Art\.|$)"
            # r")"
            r"",
            bill)
            # 'Po ust. 2 dodaje się ust. 2a w brzmieniu:')

        parts = []
        # find the fragments with these references
        for sentence in sentences:

            part = regex.findall(
                r"(?:^|\.)"
                r"(?P<senten>(?!r\.|poz.)\X*"
                r"(?:art\.|ust\.)\X*)"
                # r"(?P<rest>(?:,)\X*)"
                r"",
                sentence
            )
            if not part:
                # print("\n***\nSENT", sentence)
                # print()
                pass
            else:
                parts.append(part[0])

        rankings = []
        for fragment in parts:

            test_sentence = 'Art. 2. Bart. 1, art: 200a, 20bb. W art. 100-103 w ust. 300, 200 i 10 byyyy,' \
                            ' art. 400, 20. W art. 23 i 40, art. 30.' \
                            ' Art. 3. W art. 500: 18) ust. 1, 502-505 i 60, bo ust. 70-78. W art. 90 i 91, art. 100.'
            # art. X (, X i X-X)

            # saves ust if it follows
            # finds both if art. (X) ust. (X)
            art = regex.findall(
                r"(?P<art>\bart(?:\.|:)"  # art. lub art:
                # r"(?:(?P<big>\bArt\.\s\d+(?:\p{L}|))\X*?)?(?P<art>\bart\."
                r"(?:"
                r"(?:,\s|\s|\si\s|-|\soraz\s)"
                r"\d+(?:\p{L}*|)"
                r")+"
                r")(?:(?::\s\d+\)|:\s\p{L}+\))|:|)"  # ': a) ' lub ': 19) lub '' lub ': '
                r"(?:\s(?:w\s|)"  # 'ust.' lub 'w ust.' lub ': '
                r"(?P<ust>\bust(?:\.|:)"
                r"(?:"
                r"(?:,\s|\s|\si\s|-|\soraz\s)"
                r"\d+(?:\p{L}*|)"
                r")+)"
                # r"(?=,\s\p{L}|\.|$|:)(?<!art\.)"
                r")*"
                r"",
                # test_sentence
                fragment
            )

            # matches ust., if art. precedes, then it is matched too
            ust = regex.findall(
                r"(?:(?P<big>\bArt\.\s\d+(?:\p{L}|))\X*?)?(?:(?P<art>\bart(?:\.|:)"
                r"(?:"
                r"(?:,\s|\s|\si\s|-|\soraz\s)"
                r"\d+(?:\p{L}*|)"
                r")+"
                r")(?:(?::\s\d+\)|:\s\p{L}+\))|:|)\s)*(?:w\s|)"
                r"(?P<ust>\bust(?:\.|:)"
                r"(?:"
                r"(?:,\s|\s|\si\s|-|\soraz\s)"
                r"\d+(?:\p{L}*|)"
                r")+"
                r")",
                # test_sentence
                fragment
            )

            result = parse_articles_only(art)
            result.update(parse_paragraphs(ust))

            # ordered = sorted(result.items(), key=lambda x: x[1], reverse=True)
            # for r in ordered:
            #     print(r)

            # print(ordered)
            rankings.append(result)

    ranking = merge_references(rankings)
    print("*** RANKING ***")
    ordered = sorted(ranking.items(), key=lambda x: x[1], reverse=True)
    for r in ordered:
        print("{} - {}".format(r[1], r[0]))
    print()
    return ranking


def main():
    dir_path = 'ustawy'
    all_references = []

    n = 0
    for filename in os.listdir(dir_path):
        if n < 2000:
            all_references.append(find_references('{}/{}'.format(dir_path, filename)))
        n = n + 1

    # ranking = merge_references(all_references)
    # ordered = sorted(ranking.items(), key=lambda x: x[1], reverse=True)
    # for r in ordered:
    #     print(r)

    # for testing:
    # filename = '2000_136.txt'
    # all_references.append(find_references('{}/{}'.format(dir_path, filename)))

    # print("*** RANKING ***")
    # aggregated = aggregate_rankings(all_references)
    # print_ranking(aggregated)

main()
