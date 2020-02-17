
#DO NOT CHANGE!
def read_train_file():
	'''
	HELPER function: reads the training files containing the words and corresponding tags.
	Output: A tuple containing 'sentences' and 'tags'
	'sentences': It is a list of sentences where each sentence, in turn, is a list of words.
	For example - [['A','boy','is','running'],['Pick','the','red','cube'],['One','ring','to','rule','them','all']]
	'tags': A nested list similar to above, just the corresponding tags instead of words. 
	'''						
	f = open('train_data.txt','r')
	sentences = []
	tags = []
	sentence = []
	tag = []
	for line in f:
		s = line.rstrip('\n')
		if s == '':
			sentences.append(sentence)
			tags.append(tag)
			sentence=[]
			tag=[]
		else:
			w,t = line.split()
			sentence.append(w)
			tag.append(t)
	sentences = sentences[1:]
	tags = tags[1:]
	assert len(sentences) == len(tags)
	f.close()
	return (sentences,tags)








#NEEDS TO BE FILLED!
def store_emission_and_transition_probabilities(train_list_words, train_list_tags):
    
    '''
	This creates dictionaries storing the transition and emission probabilities - required for running Viterbi. 
	INPUT: The nested list of words and corresponding nested list of tags from the TRAINING set. This passing of correct lists and calling the function
	has been done for you. You only need to write the code for filling in the below dictionaries. (created with bigram-HMM in mind)
	OUTPUT: The two dictionaries

	HINT: Keep in mind the boundary case of the starting POS tag. You may have to choose (and stick with) some starting POS tag to compute bigram probabilities
	for the first actual POS tag.
    '''

    tag_follow_tag = {}    
    
    '''Nested dictionary to store the transition probabilities
    each tag X is a key of the outer dictionary with an inner dictionary as the corresponding value
    The inner dictionary's key is the tag Y following X
    and the corresponding value is the number of times Y follows X - convert this count to probabilities finally before returning 
    for example - { X: {Y:0.33, Z:0.25}, A: {B:0.443, W:0.5, E:0.01}} (and so on) where X,Y,Z,A,B,W,E are all POS tags
    so the first key-dictionary pair can be interpreted as "there is a probability of 0.33 that tag Y follows tag X, and 0.25 probability that Z follows X"
    '''
    word_tag = {}
    """Nested dictionary to store the emission probabilities.
	Each word W is a key of the outer dictionary with an inner dictionary as the corresponding value
	The inner dictionary's key is the tag X of the word W
	and the corresponding value is the number of times X is a tag of W - convert this count to probabilities finally before returning
	for example - { He: {A:0.33, N:0.15}, worked: {B:0.225, A:0.5}, hard: {A:0.1333, W:0.345, E:0.25}} (and so on) where A,N,B,W,E are all POS tags
	so the first key-dictionary pair can be interpreted as "there is a probability of 0.33 that A is the POS tag for He, and 0.15 probability that N is the POS tag for He"
	"""


	# *** WRITE YOUR CODE HERE ***  
    total_tag_follow_tag = 0
    count_tag_follow_tag = {}
    for sentence in train_list_tags:
        previous = '[[['
        for tag in sentence:
            try:
                count_tag_follow_tag[(previous, tag)] += 1
            except KeyError:
                count_tag_follow_tag[(previous, tag)] = 1
            previous = tag
            total_tag_follow_tag += 1
    for tags in count_tag_follow_tag:
        try:
            tag_follow_tag[tags[0]][tags[1]] = count_tag_follow_tag[tags] / total_tag_follow_tag
        except KeyError:
            tag_follow_tag[tags[0]] = {}
            tag_follow_tag[tags[0]][tags[1]] = count_tag_follow_tag[tags] / total_tag_follow_tag

    total_word_tag = {}
    count_word_tag = {}
    for tags, words in zip(train_list_tags, train_list_words):
        for tag, word in zip(tags, words):
            try:
                count_word_tag[(tag, word)] += 1
            except KeyError:
                count_word_tag[(tag, word)] = 1
            try:
                total_word_tag[tag] += 1
            except KeyError:
                total_word_tag[tag] = 1
    for tag_word in count_word_tag:
        try:
            word_tag[tag_word[0]][tag_word[1]] = count_word_tag[tag_word] / total_word_tag[tag_word[0]]
        except KeyError:
            word_tag[tag_word[0]] = {}
            word_tag[tag_word[0]][tag_word[1]] = count_word_tag[tag_word] / total_word_tag[tag_word[0]]

	# END OF YOUR CODE	

    return (tag_follow_tag, word_tag)



#NEEDS TO BE FILLED!
def assign_POS_tags(test_words, tag_follow_tag, word_tag):

    '''
	This is where you write the actual code for Viterbi algorithm. 
	INPUT: test_words - this is a nested list of words for the TEST set
	       tag_follow_tag - the transition probabilities (bigram), filled in by YOUR code in the store_emission_and_transition_probabilities
	       word_tag - the emission probabilities (bigram), filled in by YOUR code in the store_emission_and_transition_probabilities
	OUTPUT: a nested list of predicted tags corresponding to the input list test_words. This is the 'output_test_tags' list created below, and returned after your code
	ends.

	HINT: Keep in mind the boundary case of the starting POS tag. You will have to use the tag you created in the previous function here, to get the
	transition probabilities for the first tag of sentence...
	HINT: You need not apply sophisticated smoothing techniques for this particular assignment.
	If you cannot find a word in the test set with probabilities in the training set, simply tag it as 'NOUN'. 
	So if you are unable to generate a tag for some word due to unavailibity of probabilities from the training set,
	just predict 'NOUN' for that word.

    '''



    output_test_tags = []    #list of list of predicted tags, corresponding to the list of list of words in Test set (test_words input to this function)


    # *** WRITE YOUR CODE HERE *** 
    TAG_WORD_NOT_EXIST = 1e-13
    tags_set = set()
    for tag in word_tag:
        tags_set.add(tag)
    tags = []
    for tag in sorted(tags_set):
        tags.append(tag)
    for sentence in test_words:
        probability = [[[] for _ in range(len(tags))] for _ in range(len(sentence))]
        prev = [[[] for _ in range(len(tags))] for _ in range(len(sentence))]
        for i, word in enumerate(sentence):
            for j, tag in enumerate(tags):
                if i == 0:
                    try:
                        probability[i][j] = tag_follow_tag['[[['][tag] * word_tag[tag][word]
                    except KeyError:
                        probability[i][j] = tag_follow_tag['[[['][tag] * TAG_WORD_NOT_EXIST
                    prev[i][j] = -1
                else:
                    max_probability = []
                    for jj in range(len(tags)):
                        try:
                            max_probability.append(probability[i-1][jj] * tag_follow_tag[tags[jj]][tags[j]])
                        except KeyError:
                            max_probability.append(0)
                    mx = max(sorted(max_probability))
                    idx = max_probability.index(mx)
                    prev[i][j] = idx
                    try:
                        probability[i][j] = probability[i-1][idx] * word_tag[tag][word]
                    except KeyError:
                        probability[i][j] = probability[i-1][idx] * TAG_WORD_NOT_EXIST
        l = len(sentence)
        mx = max(sorted(max_probability))
        idx = max_probability.index(mx)
        ans = []
        ans.append(tags[idx])
        i = l - 1
        nx = prev[i][idx]
        i -= 1
        while nx != -1:
            ans.append(tags[nx])
            nx = prev[i][nx]
            i -= 1
        ans.reverse()
        output_test_tags.append(ans)
	# END OF YOUR CODE

    return output_test_tags









# DO NOT CHANGE!
def public_test(predicted_tags):
	'''
	HELPER function: Takes in the nested list of predicted tags on test set (prodcuced by the assign_POS_tags function above)
	and computes accuracy on the public test set. Note that this accuracy is just for you to gauge the correctness of your code.
	Actual performance will be judged on the full test set by the TAs, using the output file generated when your code runs successfully.
	'''

	f = open('public_test_data.txt','r')
	sentences = []
	tags = []
	sentence = []
	tag = []
	for line in f:
		s = line.rstrip('\n')
		if s == '':
			sentences.append(sentence)
			tags.append(tag)
			sentence=[]
			tag=[]
		else:
			w,t = line.split()
			sentence.append(w)
			tag.append(t)
	sentences = sentences[1:]
	tags = tags[1:]
	assert len(sentences) == len(tags)
	f.close()
	public_predictions = predicted_tags[:len(tags)]
	assert len(public_predictions)==len(tags)

	flattened_actual_tags = []
	flattened_pred_tags = []
	for i in range(len(tags)):
		x = tags[i]
		y = public_predictions[i]
		flattened_actual_tags+=x
		flattened_pred_tags+=y
	assert len(flattened_actual_tags)==len(flattened_pred_tags)

	correct = 0.0
	for i in range(len(flattened_pred_tags)):
		if flattened_pred_tags[i]==flattened_actual_tags[i]:
			correct+=1.0
	print('Accuracy on the Public set = '+str(correct/len(flattened_pred_tags)))



# DO NOT CHANGE!
if __name__ == "__main__":
	words_list_train = read_train_file()[0]
	tags_list_train = read_train_file()[1]

	dict2_tag_tag = store_emission_and_transition_probabilities(words_list_train,tags_list_train)[0]
	word_tag = store_emission_and_transition_probabilities(words_list_train,tags_list_train)[1]

	f = open('private_unlabelled_test_data.txt','r')

	words = []
	l=[]
	for line in f:
		w = line.rstrip('\n')
		if w=='':
			words.append(l)
			l=[]
		else:
			l.append(w)
	f.close()
	words = words[1:]
	test_tags = assign_POS_tags(words, dict2_tag_tag, word_tag)
	assert len(words)==len(test_tags)

	public_test(test_tags)

	#create output file with all tag predictions on the full test set

	f = open('output.txt','w')
	for i in range(len(words)):
		sent = words[i]
		pred_tags = test_tags[i]
		for j in range(len(sent)):
			word = sent[j]
			pred_tag = pred_tags[j]
			f.write(word+' '+pred_tag)
			f.write('\n')
		f.write('\n')
	f.close()

	print('OUTPUT file has been created')	
