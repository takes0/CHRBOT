import time
import random
import Text2Emotion as te
import requests
import sys


def main():
    while True:
        lock = input("Would you like to go on y/n? ")
        if lock.lower() == "y":
            asked_phrase = input("Type something: ")
            try:
                title, phrase = film_search(asked_phrase)

                response = answer_extract(title, phrase)
            except:
                continue
            else:
                break
        elif lock.lower() == "n":
            sys.exit()
        else:
            continue

    if type(response) == tuple:
        emoji1 = emotion_checker(response[0])
        emoji2 = emotion_checker(response[1])
        print(f"{response[0]}{emoji1}\n{response[1]}{emoji2}")
    else:
        emoji1 = emotion_checker(response)
        print(response, emoji1)


# serching for film with text
def film_search(text):
    nmbr = -1

    while True:
        try:
            # get result
            response = requests.get(
                f"https://api.quodb.com/search/{text}?advance-search=false&keywords="
                "&titles_per_page=100&phrases_per_title=1&page=1"
            )
            result_list_dict = response.json()
            result_list = result_list_dict["docs"]

            # getting random film
            film_dict = result_list[random.randrange(0, len(result_list))]
            title_id = film_dict.get("title_id")
            phrase_id = film_dict.get("phrase_id")
            print("")
            return title_id, phrase_id

        # ERRORS place
        except (ValueError, KeyError):
            if len(text.split()) == 0:
                print("/n")
                raise Exception()

            elif len(text.split()) > 1:
                text = text.rsplit(" ", 1)[0]
                continue

            else:
                nmbr += 1
                text = text[:-1]

                time.sleep(0.25)
                print("." * nmbr, end="", flush=True)
                continue


# answer from film
def answer_extract(title_id, phrase_id):
    # getting phrase
    info = requests.get(f"https://api.quodb.com/quotes/{title_id}/{phrase_id}")
    answer_dict = info.json()

    # printing next phrase
    params = answer_dict["docs"]
    for i, param in enumerate(params):
        # params has hundreds of elements we will stop on 100th
        if i < 100:
            # ????
            if param["phrase_id"] == phrase_id:
                answer = params[i + 1]["phrase"]

                if answer.startswith((" ", "-")):
                    # print('starts with " ", "-"')
                    return answer.replace("-", "")
                # question
                elif answer.endswith(("?")):
                    # print('ends with "?"')
                    answer1 = params[i + 1]["phrase"]
                    return answer1
                # halfphrase
                elif answer.endswith(("...", "!")):
                    # print('ends with "...", "!"')
                    answer1 = params[i + 1]["phrase"]
                    answer2 = params[i + 2]["phrase"]
                    return answer1, answer2
                # normalcase
                else:
                    return answer
                break


# cheking emotion and converting to emoji
def emotion_checker(text):
    emotions = te.get_emotion(text)

    # hardcoding emojis in dict
    emotions["😊"] = emotions.pop("Happy")
    emotions["😡"] = emotions.pop("Angry")
    emotions["😯"] = emotions.pop("Surprise")
    emotions["😞"] = emotions.pop("Sad")
    emotions["😨"] = emotions.pop("Fear")

    # emoji atribution
    if all(value == 0 for value in emotions.values()):
        top_emotion = ""
        return top_emotion
    else:
        top_emotion = max(emotions, key=emotions.get)
        return top_emotion


if __name__ == "__main__":
    main()
