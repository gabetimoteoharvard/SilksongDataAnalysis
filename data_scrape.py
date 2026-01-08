import requests
import os 
import json

PARAMS = {
    'json':1,                                       
    'language': 'english',
    'cursor': '*',                                  
    'num_per_page': 100,                            
    'filter': 'recent'
}

APP_ID = 1030300 # Silksong steam ID

def get_user_reviews(review_appid, params):
    url = f'https://store.steampowered.com/appreviews/{review_appid}'
    

    req_user_review = requests.get(
        url,
        params=params
    )
    if req_user_review.status_code != 200:
        print(f'Fail to get response. Status code: {req_user_review.status_code}')
        return {"success": 2}
    
    try:
        user_reviews = req_user_review.json()
    except:
        return {"success": 2}
    
    return user_reviews

def get_bulk_reviews(app_id, PARAMS, page_numbers=1):
    page = 0

    reviews_dict = { "query_summary": {
                           "num_reviews": 0, 
                           "total_positive": 0,
                           "total_negative": 0,
                    },
                    "reviews": []
                   }

    while page < page_numbers:
        reviews_response = get_user_reviews(app_id, PARAMS)

        if reviews_response["success"] != 1:
            print("Not a success")
            print(reviews_response)

        if reviews_response["query_summary"]['num_reviews'] == 0:
            print("No reviews.")
            print(reviews_response)
        
        for review in reviews_response["reviews"]:
            reviews_dict["query_summary"]["num_reviews"]+=1

            reviews_dict["reviews"].append(review)

            if review["voted_up"]:
                reviews_dict["query_summary"]["total_positive"]+=1
            else:
                reviews_dict["query_summary"]["total_negative"]+=1
             
         # go to next page
        try:
            cursor = reviews_response['cursor']         # cursor field does not exist in the last page
        except Exception as e:
            cursor = ''

        if not cursor:
            print("Reached the end of all comments.")
            break
    
        # set the cursor object to move to next page to continue
        PARAMS['cursor'] = cursor
        page+=1
       
    
    PARAMS['cursor'] = '*'

    return reviews_dict


def make_json_file(review_dict, filename="data"):
    try:
        with open(os.getcwd() + f'/{filename}', 'w') as json_file:
            json.dump(review_dict, json_file, indent=4)

        print(f'Made JSON file at /{filename} .')
        return 0
    except Exception as e:
        print(f'Unable to make JSON file. Following error has occurred: {e}')
        return 1



def main():
    number_of_pages = 2000
    silksong_reviews = get_bulk_reviews(APP_ID, PARAMS, page_numbers=number_of_pages)

    make_json_file(review_dict=silksong_reviews, filename="skong")

    return 0
    

if __name__ == "__main__":
    main()