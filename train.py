class textbot:
    
    def __init__(self,text):
        import tensorflow as tf
        import pickle
        self.text = text
        enc_model= tf.keras.models.load_model("/model/encoder")
        dec_model= tf.keras.models.load_model("/model/decoder")
        # Initialization of variables preprocessed in model
        self.maxlen_questions =22
        self.VOCAB_SIZE =1975
        self.maxlen_answers =172
        self.text = text
        with open('model/tokenizer.pickle', 'rb') as handle:
            self.tokenizer = pickle.load(handle)

    def preprocess_input(self):
        from keras_preprocessing.sequence import pad_sequences
        import string
        s=self.text.translate(str.maketrans('', '', string.punctuation))
        tokens = s.lower().split()
        tokens_list = []
        for word in tokens:
            tokens_list.append(self.tokenizer.word_index[word]) 
        return pad_sequences([tokens_list] , maxlen=self.maxlen_questions , padding='post')


    

    def test(self):

        import numpy as np
        states_values = self.enc_model.predict(self.preprocess_input())
        empty_target_seq = np.zeros((1 , 1))
        empty_target_seq[0, 0] = self.tokenizer.word_index['start']
        stop_condition = False
        decoded_translation = ''
        
        while not stop_condition :
            dec_outputs , h , c = self.dec_model.predict([empty_target_seq] + states_values)
            sampled_word_index = np.argmax(dec_outputs[0, -1, :])
            sampled_word = None
                
            for word , index in self.tokenizer.word_index.items() :
                if sampled_word_index == index :
                    decoded_translation += f' {word}'
                    sampled_word = word
                
            if sampled_word == 'end' or len(decoded_translation.split()) > self.maxlen_answers:
                stop_condition = True
                    
            empty_target_seq = np.zeros((1 , 1))  
            empty_target_seq[0 , 0] = sampled_word_index
            states_values = [h , c] 
        decoded_translation = decoded_translation.split(' end')[0]
        return decoded_translation.lstrip().capitalize()


class imgbot:

    def send_task_to_dream_api(prompt, style_id=16, target_img_path=None):
        import requests
        import json
        import time
        from PIL import Image
        BASE_URL = "https://api.luan.tools/api/tasks/"
        HEADERS = {
            'Authorization': 'bearer x1AcemRCQU9Jrz9A0hsWElX9TDE5eDeA',
            'Content-Type': 'application/json'
        }
        """
        Send requests to the dream API.
        prompt is the text prompt.
        style_id is which style to use (a mapping of ids to names is in the docs).
        target_img_path is an optional path to an image to influence the generation.
        """

        # Step 1) make a POST request to https://api.luan.tools/api/tasks/
        post_payload = json.dumps({
            "use_target_image": bool(target_img_path)
        })
        post_response = requests.request(
            "POST", BASE_URL, headers=HEADERS, data=post_payload)
        
        # Step 2) skip this step if you're not sending a target image otherwise,
        # upload the target image to the url provided in the response from the previous POST request.
        if target_img_path:
            target_image_url = post_response.json()["target_image_url"]
            with open(target_img_path, 'rb') as f:
                fields = target_image_url["fields"]
                fields ["file"] = f.read()
                requests.request("POST", url=target_image_url["url"], files=fields)

        # Step 3) make a PUT request to https://api.luan.tools/api/tasks/{task_id}
        # where task id is provided in the response from the request in Step 1.
        task_id = post_response.json()['id']
        task_id_url = f"{BASE_URL}{task_id}"
        put_payload = json.dumps({
            "input_spec": {
                "style": style_id,
                "prompt": prompt,
                "target_image_weight": 0.1,
                "width": 960,
                "height": 1560
        }})
        requests.request(
            "PUT", task_id_url, headers=HEADERS, data=put_payload)
        # Step 4) Keep polling for images until the generation completes
        while True:
            print('generating a picture......')
            response_json = requests.request(
                "GET", task_id_url, headers=HEADERS).json()

            state = response_json["state"]

            if state == "completed":
                r = requests.request(
                    "GET", response_json["result"])
                with open("image.jpg", "wb") as image_file:
                    image_file.write(r.content)
                im = Image.open('image.jpg')
                im.show()
                break

            elif state =="failed":
                print("generation failed :(")
                break