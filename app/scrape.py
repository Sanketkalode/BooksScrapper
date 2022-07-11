from app.exit_ops import save_to_file


def get_coverImage(bs):
    try:
        return bs.find('img', id='coverImage')['src']

    except TypeError:
        try:
            save_to_file(bs.title.text, 'coverImage')
            return bs.find('img', {'class': 'BookCover__image'})['src']
            pass
        except:
            return 'https://url_not_available.com'


def get_description(bs):
    global description
    try:
        description = bs.find('div', id='description')
        if description is not None:
            desc_span = description.find('span', style='display:none')
            return desc_span.text
        else:
            description = bs.find('div', {'class': 'TruncatedText__text TruncatedText__text--5 '
                                                   'TruncatedText__text--expanded'})
            if description is not None:
                desc_span = description.find('span', {'class': 'Formatted'})
                return desc_span.text
    except TypeError and AttributeError:
        save_to_file(bs.title.text, 'Description')
        return 'Description not Available'
        pass


def get_genre(bs):
    try:
        genre = bs.find_all('div', {'class': 'bigBoxBody'})
        genre_l = genre[6].find_all('div', {'class': 'left'})
        genre_list = []
        for gl in genre_l:
            genre_list.append(gl.a.text)
        return genre_list
    except Exception:
        save_to_file(bs.title.text, 'Genre List')
        print('Genre not found')
        return []
        pass


def get_otherEditons(bs):
    global otheredition
    other_edition_list = []
    try:

        if bs.find('div', {'class': 'otherEditionCovers'}) is not None:
            otheredition = bs.find('div', {'class': 'otherEditionCovers'})
        else:
            otheredition = bs.find('div', {'class': 'EditionDetails'})

        edts = otheredition.find_all('a')

        for e in edts:
            other_edition_list.append(e.img['alt'])
    except AttributeError:
        other_edition_list = []

    return other_edition_list


def get_otherEditonsCovers(bs):
    global otheredition
    other_edition_cover_list = []
    try:
        if bs.find('div', {'class': 'otherEditionCovers'}) is not None:
            otheredition = bs.find('div', {'class': 'otherEditionCovers'})
        else:
            other_edition = bs.find('div', {'class': 'EditionDetails'})
        edts = otheredition.find_all('img')

        for e in edts:
            other_edition_cover_list.append(e['src'])
    except AttributeError:
        other_edition_cover_list = []

    return other_edition_cover_list


def get_seriesList(bs):
    try:
        series_list = []
        serie_list = bs.find('div', {'class': 'seriesList'})
        if serie_list is not None:
            sr_list = serie_list.find_all('img')
            for sl in sr_list:
                series_list.append(sl['alt'])

        return series_list
    except AttributeError:
        save_to_file(bs.title.text, 'Series List')
        return []
        pass


def get_seriesListCovers(bs):
    try:
        series_list_cover = []
        serie_list = bs.find('div', {'class': 'seriesList'})
        if serie_list is not None:
            sr_list = serie_list.find_all('img')
            for sl in sr_list:
                series_list_cover.append(sl['src'])

        return series_list_cover
    except AttributeError:
        save_to_file(bs.title.text, 'Series List Covers')
        return []
        pass


def get_bookUrl(url, bookId, title):
    title = clean_title(title)
    book_url = url + str(bookId) + '.' + title
    print(book_url)
    return book_url


def clean_title(title):
    if ' (' in title:
        title = title.split(" (")[0]
    if "'" in title:
        title = title.replace("'", "")
    if ":" in title:
        title = title.split(":")[0]

    title = title.replace(' ', '_')
    return title


def get_username(bs, count):
    try:
        us = bs.find_all('div', {'class', 'review'})
        name = us[count].find('a', {'class': 'left imgcol'})
        return name['title']
    except AttributeError:
        return 'User'
    except IndexError:
        pass


def get_reviewDate(bs, count):
    try:
        rd = bs.find_all('div', {'class', 'review'})
        date = rd[count].find('a', {'class': 'reviewDate createdAt right'})
        return date.text
    except AttributeError:
        from datetime import datetime
        return datetime.today().strftime('%Y-%m-%d')
    except IndexError:
        pass


def get_rating(bs, count):
    rating_dict = {
        'did not like it': 1,
        'it was ok': 2,
        'liked it': 3,
        'really liked it': '4',
        'it was amazing': '5'
    }

    try:
        rat = bs.find_all('div', {'class', 'review'})
        rating = rat[count].find('span', {'class': 'staticStars notranslate'})

        return rating_dict[rating['title']]
    except IndexError:
        pass
    except Exception:
        pass


def get_review(bs, count):
    try:
        rev = bs.find_all('div', {'class', 'review'})
        try:
            review = rev[count].find('div', {'class': 'reviewText stacked'})
        except IndexError:
            pass
        review = review.find_all('span')
        return review[2].text
    except IndexError:
        return review[1].text
    except Exception:
        return "No Comments"
