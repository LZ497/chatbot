### Table of Contents
- [Introduction](#introduction)
- [Methodology](#methodology)
- [Deployment](#deployment)
- [Conclusion](#conclusion)



# Introduction

**1. Description**  
Through chatbot, people can communicate with virtual assistant. Through our chatbot, communication was not limited to textual conversation, but can be conducted with pictures and voices consider some vision impairments. In ther words, we have implemented three basic functions in this project, text, image and vocie.  
First, we can text chat with chatbot and send basic daily life questions to chatbot and get very precise answers. This function is implemented by relying on the LSTM model in neural networks. The second function is that we send a descriptive text to chatbot and it will return a corresponding beautiful picture to us. This function is implemented by relying on the Wombo API. The third function is to communicate with the chatbot by voice, which is a virtual but realistic person generated by Audio2Face, an open sources software under NVIDIA. We can have a voice conversation with the chatbot, and it make response with auto lip-synic.

**2. Data**  
Text Dataset:  
https://www.kaggle.com/datasets/kausr25/chatterbotenglish  
https://www.kaggle.com/datasets/saurabhprajapat/chatbot-training-dataset 



# Methodology
**1. LSTM Model**  
To fills the slots and predicts the intent in the same time, we chose a sequence-to-sequence model using bidirectional LSTM network. Actually, the model is doing the same using an attention-based RNN.
Frist we reduce the redundant words if the answer has two or more of them desides removing stopwords. After cleaning data and appending <START> and <END> in all sequences, we tokenized using Word2Vec in gensim and paded the questions and answers using a single vocabulary. Using one-hot encoding answers.Trained a basic LSTM-based Seq2Seq model to predict decoder_target_data given encoder_input_data and decoder_input_data. Decode some sentences to check that the model is working (i.e. turn samples from encoder_input_data into corresponding samples from decoder_target_data).
![NN model summary](/model.png)  
Picture 1 NN model summary  
**2. Picture Generator**  
Wombo, like many other apps that create generative art, is basically based on two artificial neural networks that work together to create the images, which are VQGAN and CLIP. VQGAN is a neural network used to generate images that look similar to other images. CLIP, on the other hand, is a neural network trained to determine how well a text description fits an image. CLIP provides feedback to VQGAN on how best to match the image to the text prompt. VQGAN adjusts the image accordingly and passes it back to CLIP to check how well it fits the text. This process is repeated a few hundred times, resulting in the ki-generated images. Since the model has already been well-pretrained by Wombo, so the best and easist way to do this is using Wombo API to utilize the model inside.  
<img src="./image.jpg" width = "300" align=center/>  
Picture 2 given instruction: "picture: a cat looks like a dog"   
**3. Speaking Version**  
To achieve Speaking Version chatbot, we need to clarify there are steps. Frist, with the help of the “Speech Recognition” API and “PyAudio” library, we built automatic speech recognition model to convert our speech to text. And then, text is passed into GPT3 model to get a quick response. After getting text response, we used gTTS library to generate audio file. In the end, audio file is converted to numpy type and feeded in Omniverse Audio2Face. Audio2Face is a combination of artificial intelligence (AI)-based technologies that derive facial motion and lip sync animations from an audio source. 
<img src="picture/audio2face.png" width = "800" align=center/> 
Picture 3 NN model summary  



# Deployment

**1. Text Version**  
After saving our trained model, we used flask to deploy our chatbot system locally.  

**2. Speaking Version** 
Audio2Face
# Conclusion