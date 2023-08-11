class Speech:
    
    def __init__(self,year,theme,speaker,transcript):
        self.year = year
        self.theme = theme
        self.speaker = speaker
        self.transcript = transcript
        
        
    def tokenizer(self,*speech_tokens):
        """
        This function tokenizes the text.
        It retrieves the transcript, and splits up the text into tokens
        """
        speech_tokens = word_tokenize(self.transcript)
        
        return speech_tokens
        
    def lowercase(self,*lowerspeech_tokens):
        """
        This function lowercases the speech tokens. 
        It calls upon the tokenizer function, retrieves the tokens
        then lowercases them
        """        
        lowerspeech_tokens = [word.lower()
                        for word in self.tokenizer(self.transcript)]
        
        return lowerspeech_tokens
        
    def uppercase(self,*upperspeech_tokens):
        
        """
        This function uppercases the speech tokens.
        Works the same as "lowercase"
        
        """
        upperspeech_tokens = [word.upper()
                             for word in self.tokenizer(self.transcript)]
        
        return upperspeech_tokens
        
    def frequency_statistics(self,plot:bool=False):
        """
        This function takes in text, returns the FreqDist for the chosen text
        If plot=True, it will plot the 25 most common tokens in the text.
        
        """
        frequencies = FreqDist(self.lowercase(self.transcript))
        
        if plot==True:
            frequencies.plot(25,title='Frequency distribution for the 25 most common tokens in our text collection')
        
        return frequencies 
    
    def textcleaning(self,extraremovals= None,*frequencies_filtered,plot:bool=False):
        """
        Text cleaner function, that takes in text, removes the stopwords and punctuation and digits,
        It also takes in a list of words the user would like removed in "removals", if this is left empty the function
        still runs.
        If plot is true, it will plot the frequencies for the tokens after the removals have been made. 
        """
        if extraremovals == None:
            extraremovals = []
        
        remove_these = set(stopwords.words('english') + list(string.punctuation) + list(string.digits)+list(extraremovals))
        
        filtered_speech = [token 
                 for token in self.lowercase(self.transcript) 
                 if not token in remove_these]
        
        frequencies_filtered = FreqDist(filtered_speech)
        
        if plot==True:
            frequencies_filtered.plot(25,title='Frequency distribution (excluding stop words, digits, and punctuation)')
        
        return frequencies_filtered
    
    def wordcloudgenerator(self,textfreq=None,mask=None):
        """
        Generates a word cloud using the text frequencies returned by the FreqDist function.
        You may pass a text frequency argument.
        If textfreq is left as none then the function will fetch the text frequencies from the transcript directly.
        These text frequencies may not be 'cleaned' and may still contain punctuation.
        
        A mask image may be passed to shape the wordcloud into a certain shape.
        Alternatively no mask image may be passed to generate a square-shaped wordcloud.
        """
        if textfreq is None:
            textfreq = self.frequency_statistics(plot=False)
        

        countedtext = Counter(textfreq)
        
        if mask is None:
            cloud = WordCloud(width=800, height=400, max_font_size=160, background_color= "white", colormap= "RdYlGn").generate_from_frequencies(countedtext)
            plt.figure(figsize=(16,12))
            plt.imshow(cloud,interpolation='bilinear')
            plt.axis('off')
            plt.show()
            
            
        elif mask is not None:
            if type(mask)!=numpy.ndarray:
                mask = np.array(mask)
                
            cloud = WordCloud(width=1000, height=600, max_font_size=200, background_color= "white", colormap= "RdYlGn",mask=mask).generate_from_frequencies(countedtext)
            plt.figure(figsize=(16,12))
            plt.imshow(cloud,interpolation='bilinear')
            plt.axis('off')
            plt.show()
            
        return cloud
