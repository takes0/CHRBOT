from project import film_search, answer_extract, emotion_checker
import pytest


# test api --- I/O => text/title_id,phrase_id
def test_film_search():
    text1 = film_search("How are you")
    assert isinstance(text1[0], str)
    assert isinstance(text1[1], int)

    text2 = film_search("Habrakadabar")
    assert isinstance(text2[0], str)
    assert isinstance(text2[1], int)

    with pytest.raises(Exception):
        film_search("@")
    with pytest.raises(Exception):
        film_search("")


# test answer --- I/O => title_id,phrase_id/text
def test_answer_extract():
    phrase1 = answer_extract("M253038555", 24290586)
    assert isinstance(phrase1, (tuple, str))

    phrase2 = answer_extract("M52256b63f", 40142888)
    assert isinstance(phrase2, (tuple, str))

    phrase3 = answer_extract("M670978896", 51486112)
    assert isinstance(phrase3, (tuple, str))


# emotion test --- I/O => text/emoji
def test_emotion_checker():
    assert emotion_checker("She's flying high after the successful interview.") == "😨"
    assert (
        emotion_checker("I don't know. You left and all of a sudden I'm in the middle of West Side Story."
        ) == "😯")
    assert (
        emotion_checker("Thank God, you did not have Urdu paper. Get lost you fool!"
        )== "😞")
    assert (
        emotion_checker("Hear him roar, see him foam But we're not coming home"
        ) == "😡")
    assert (
        emotion_checker("Detective, nice of you to come here, seeing how every cop is looking for you."
        ) == "😊")
    assert emotion_checker("Hello, John.") == ""
