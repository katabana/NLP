import regex
import os


class Reference:

    def __init__(self, year, position, title='', number=None):
        self.id = "{}_{}".format(year, position)
        self.year = year
        self.position = position
        self.title = title
        self.number = number

    def __str__(self):
        if self.title:
            return "{} r., Nr {}, poz. {} {}".format(self.year, self.number,  self.position, self.title)
        else:
            return "{} r., Nr {}, poz. {}".format(self.year, self.number,  self.position)

    def __repr__(self):
        if self.title:
            return "\n{}: {}, Nr {}, poz. {} - {}".format(self.id, self.year, self.number, self.position, self.title)
        else:
            return "\n{}: {}, Nr {}, poz. {}".format(self.id, self.year, self.number, self.position)


# can be a number but not necessarily
# year is obligatory, but not always given
# position is essential

#  Solutions to problems
#  Dz.Urz. => do nothing about that
#  do not consider things like 'Przepisy art. 6 ust. 1 i 2 ustawy, o której mowa w art. 4 (...)'
#  'o .*' is not efficient enough for the title
#  sometimes Dz.U. sometimes Dz. U. => watch whitespaces

def find_title(year, titles):
    title = None
    if year in titles:
        title = titles[year]
        not_real_title = (regex.match(r'^Zmiany\X*', title)) or \
                         (regex.match(r'^[\t\p{Zs}\xA0\n]*Nr\X*', title)) or \
                         (regex.match(r'^\d\X*', title))
        if not_real_title:
            title = None
    return title


def find_year_separated(intro_year, bill_year, sentence, part, titles):

    bill = sentence + ' ' + part

    # if no year after 'Dz. U.' returns
    without_year = regex.findall(r"Dz\.[\t\p{Zs}\xA0\n]*U\.[\t\p{Zs}\xA0\n]*"  # Dz. U.
                                 r"(?=Nr|poz)(?P<content>.+?(?=[\t\p{Zs}\xA0\n]z|$))", sentence)  # avoid year

    year_separated = regex.findall(r"z[\t\p{Zs}\xA0\n]*"  # 'z '
                                   r"(?P<year>\w{4})[\t\p{Zs}\xA0\n]*r.[\t\p{Zs}\xA0\n]*"  # 'XXXX r. '
                                   r"(?P<content>\X*)",
                                   bill, overlapped=True)

    records = []

    # if the year is not given in the bill
    if without_year:

        if not bill_year:
            # if not found, check whether numbers are correct?
            if not intro_year:
                dots = regex.findall(r'(?:Nr|poz\.)(?:[\t\p{Zs}\n]*\.{3})', part)
                if dots:
                    pass
                else:
                    # print("w/o year", sentence)
                    # print(part)
                    pass
            else:
                title = find_title(intro_year, titles)
                records.append((intro_year, without_year[0], title))
        else:
            title = find_title(intro_year, titles)
            records.append((intro_year, without_year[0], title))
            pass

    if year_separated:
        for year, content in year_separated:
            title = find_title(year, titles)
            c = regex.search(r".+?(?=[\t\p{Zs}\xA0\n]z|$)", content)
            records.append((year, c.group(0), title))
            # print('{} r.: {}'.format(year, c.group(0)))

    # print(records)
    return records


def find_year_in_text(text):
    return regex.findall(r"(\d{4}) r.", text)


# split to find a year of the bill in its reference and get the content
def create_year_references(years_list):
    records = []
    for year, content, title in years_list:
        # for getting (year, positions) Nr x, [poz. a-b, poz. a i b, poz. a, b i c] (może być bez przecinka po numerze)
        c = regex.findall(r"(?:Nr[\t\p{Zs}]*(?P<number>\d+),){,1}"  # to get 'Nr X,'
                          r"[\t\p{Zs}]*poz.[\t\p{Zs}]*"  # to get ' poz. '
                          r"(?P<pos>\d+(?:[-]{,1}\d+|[\t\p{Z}]*[,i][\t\p{Z}]*\d+)*)",
                          content)   # working example 'Nr 120, poz. 121, 123-125, 130 i 144-150'

        records += create_references(year, c, title)
    return records


def separate_positions(positions):
    # separate by 'i' and commas
    separated = []
    positions = regex.split(r"[\t\p{Zs}]*i[\t\p{Zs}]*|,[\t\p{Zs}]*", positions)
    for position in positions:
        if '-' in position:  # make range of references
            [start, end] = regex.split(r"-", position)
            for i in range(int(start), int(end) + 1):
                separated.append(str(i))
        else:
            separated.append(position)
    return separated


def create_references(year, refs, title):
    references = []
    for ref in refs:
        positions = ref[1]
        # separate by commas
        split_positions = separate_positions(positions)

        for position in split_positions:
            # if the number is not empty
            if not ref[0]:
                references.append(Reference(year, position, title=title))
            else:
                references.append(Reference(year, position=position, number=ref[0], title=title))
    # print(result)
    return references


def aggregate(references):
    aggregated = {}
    for ref in references:
        if ref.id in aggregated.keys():
            n, val = aggregated[ref.id]
            aggregated[ref.id] = (n + 1, val)
        else:
            aggregated[ref.id] = (1, ref)
    return aggregated


def print_ranking(dict):
    for key, value in sorted(dict.items(), key=lambda x: x[1][0], reverse=True):
        print("{} - {}: {}".format(value[0], key, value[1]))


def find_references(filepath):
    # print(filepath)
    references = []

    with open(filepath, 'r') as bill_file:
        bill = bill_file.read()
        bill = regex.sub(r'[\t\p{Zs}\xA0\n]+', ' ', bill)  # remove redundant spaces

        sentences = regex.findall(
            r"(?P<sent>(?:^|\.|\p{Lu})[\t\p{Zs}\xA0\n]*" 
            # r"\X{,400}?"   # TODO : pick a number! for long sentences
            r"\X*?"  
            r"(?:"
            r"(?=\)"
            r"|(?=\.[\t\p{Zs}\xA0\n]*(?!U\.|Nr)(?:\p{Lu}|$)))"
            r"))",
            bill
            # 'Zmiany wymienionej ustawy zostały 2000 roku ogłoszone w (Dz.U. z 2016 r. poz. Nr 2225 oraz z \n'
            # '2017 r. poz. 88, 244, 379, 708, 768, 1086 i 1321.\n'
            # 'Zdanie po nic. '
            # 'Art. 44 ustawy z dnia 13 lipca \n1980 roku o prywatyzacji przedsiębiorstw państwowych (Dz.U. Nr 522, poz.'
            # '\n298 oraz z 1991 r. Nr 60, poz. 253 i Nr 111, poz. 480) z wyłączeniem'
            # '\nprzepisów art. 19 ust. 1 zdanie drugie i art. 28. U 4 ustawy z dnia 13 lipca '
            # '\n1990 r. o prywatyzacji przedsiębiorstw państwowych (Dz.U. Nr 51, poz.'
            # '\n298 oraz z 1991 r. Nr 60, poz. 253 i Nr 111, poz. 480) z wyłączeniem'
            # '\nprzepisów art. 19 ust. 1 zdanie drugie i art. 28.'
            # 'Zdanie to 2000 r. ar 1)Dz. U. Nr 20. Tak to jest, że poz. 20 i nic. Zdanie 3 (bo tak) wypada.'
        )

        # print(sentences)
        # exit(0)

        parts = []
        for sentence in sentences:
            part = regex.findall(
                r"(?:^|\.)"
                r"(?P<senten>(?!r\.|poz.)\X*?"
                r"(?=\X*?(?P<year1>\d{4}))*\X*?"  # may contain a year
                r"(?P<dz>(?:Dz\.[\t\p{Zs}\xA0\n]*U\.[\t\p{Zs}\xA0\n]*)"  # Dz. U.
                r"(?:.*?(?:(?P<year2>\d{4})?[\t\p{Zs}\xA0\n]*(?:roku|r\.))))"  # po Dz. U.: '(...) XXXX roku\r. '
                r"(?P<rest>\X*))",
                sentence
                # 'dlugie zdanie\n bo czemu nie\n Dz. U. Nr ... 1994 r.'
            )
            if part:
                # print("part", part)
                parts += part
            else:
                # print("part", sentence)
                # exit(0)
                pass

        for intro, intro_year, bill_text, bill_year, part in parts:
            # print("{}: {}".format(bill_year, bill_text))

            if not bill_text:
                print('err')

            part = part.replace('\n', ' ')
            bill_text = bill_text.replace('\n', ' ').replace('(', '').replace('\s\s+', '\s')

            # crop right side
            cropped = regex.findall('(?P<title>\X*?)'
                                    '[\t\p{Zs}\xA0\n]*\(*Dz\.[\t\p{Zs}\xA0\n]*U\.',  # '  Dz.' lub ' (Dz. U.'
                                    intro)

            titles = {}
            for title_part in cropped:
                title_part = regex.sub(r'[\t\p{Zs}\xA0\n]+', ' ', title_part)  # remove redundant spaces
                title_part = regex.sub(r'^\.[\t\p{Zs}\xA0\n]*', '', title_part)  # delete '.' at the beginning
                title = regex.findall('(?P<year>\d{4})*(?:[\t\p{Zs}\xA0\n]+roku[\t\p{Zs}\xA0\n]+|'   # match 'roku'
                                      '[\t\p{Zs}\xA0\n]*r\.)'  # match ' r.'
                                      '(?!\X*'  # do not repeat
                                      '(?:[\t\p{Zs}\xA0\n]*r\.|'  # match ' r.'
                                      '[\t\p{Zs}\xA0\n]+roku[\t\p{Zs}\xA0\n]+))'  # match ' roku '
                                      '(?P<title>\X*)',  # get title
                                      title_part)
                                      # 'W ustawie z 2003 r., Maroku i z 2001 roku  - Prawo farmaceutyczne Dz. U. ')

                if title:
                    title_year, title_content = title[-1]
                    titles[title_year] = title_content
                else:
                    titles[bill_year] = title_part

            results = find_year_separated(intro_year, bill_year, bill_text, part, titles)
            references += create_year_references(results)

        # print("refs", references)
        # exit(0)

    # aggregate the results
    aggregated = aggregate(references)
    # print_ranking(aggregated)
    return aggregated


def aggregate_rankings(rankings):
    aggregated = {}
    for ranking in rankings:
        for ref in ranking:
            if ref in aggregated.keys():
                n, val = aggregated[ref]
                aggregated[ref] = (n + 1, val)
            else:
                aggregated[ref] = (ranking[ref])
    return aggregated


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

    print("*** RANKING ***")
    aggregated = aggregate_rankings(all_references)
    print_ranking(aggregated)

main()
