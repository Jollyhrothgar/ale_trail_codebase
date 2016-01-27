import random

beer_quotes = [
{
'quote':'The problem with the world is that everyone is a few drinks behind',
'name':'Humphrey Bogart',
},
{
'quote':'Always do sober what you said you would do drunk.  That will teach you to keep your mouth shut.' ,
'name':'Earnest Hemingway',
},
{
'quote':'Beer is proof that God loves us and wants us to be happy.' ,
'name':'Benjamin Franklin',
},
{
'quote':'He is a wise man who invented beer.' ,
'name':'Plato',
},
{
'quote':'I feel sorry for people who don\'t drink. When they wake up in the morning, that\'s as good as they\'re going to feel all day.' ,
'name':'Frank Sinatra',
},
{
'quote':'Give me a woman who loves beer and I will conquer the world. ' ,
'name':'Kaiser Wilhelm',
},
{
'quote':'I would kill everyone in this room for a drop of sweet beer.' ,
'name':'Homer Simpson',
},
{
'quote':'Without question, the greatest invention in the history of mankind is beer. Oh, I grant you the wheel was also a fine invention, but the wheel does not go nearly as well with pizza.' ,
'name':'Dave Berry',
},
{
'quote':'24 hours in a day, 24 beers in a case. Coincidence?' ,
'name':'Stephen Wright',
},
{
'quote':'Everybody has to believe in something.....I believe I\'ll have another drink.' ,
'name':'W.C. Fields',
},
{
'quote':'May your glass be ever full. May the roof over your head be always strong. And may you be in heaven half an hour before the devil knows you\'re dead.' ,
'name':'Irish Toast',
},
{
'quote':'You can\'t be a real country unless you have a beer and an airline - it helps if you have some kind of a football team, or some nuclear weapons, but at the very least you need a beer.' ,
'name':'Frank Zappa',
},
{
'quote':'I am a firm believer in the people. If given the truth, they can be depended upon to meet any national crisis. The great point is to bring them the real facts, and beer.',
'name':'Abraham Lincoln',
},
{
'quote':'An intelligent man is sometimes forced to be drunk to spend time with his fools.',
'name':'Earnest Hemingway',
},
{
'quote':'Always remember that I have taken more out of alcohol than alcohol has taken out of me.',
'name':'Winston Churchill',
},
{
'quote':'Ah, beer. The cause of, and solution to all of life\'s problems.',
'name':'Homer Simpson',
},
{
'quote':'Beer makes you feel the way you ought to feel without beer.',
'name':'Henry Lawson',
},
{
'quote':'I would give all my fame for a pot of ale and safety.',
'name':'Shakespeare, \'Henry V',
},
{
'quote':'God made yeast, as well as dough, and loves fermentation just as dearly as he loves vegetation.',
'name':'Ralph Waldo Emerson',
},
{
'quote':'Drunkenness does not create vice; it merely brings it into view.',
'name':'Seneca',
},
{
'quote':'The good Lord has changed water into wine, so how can drinking beer be a sin?',
'name':'Sign near a Belgian Monastary',
},
{
'quote':'A man can hide all things, excepting twain - That he is drunk, and that he is in love.',
'name':'Antiphanes',
},
{
'quote':'I work until beer o\'clock',
'name':'Stephen King ',
},
{
'quote':'He that drinketh strong beer and goes to bed right mellow, lives as he ought to live and dies a hearty fellow.',
'name':'Anonymous',
},
{
'quote':'Tis hard to tell which is best: music, food, beer or rest.',
'name':'Anonymous',
},
{
'quote':'Beer... Now there\'s a temporary solution.',
'name' :'Homer Simpson',
},
{
'quote':'Work is the curse of the drinking classes.',
'name':'Oscar Wilde',
},
{
'quote':'Beauty lies in the hands of the beerholder.',
'name':'Anonymous',
},
{
'quote':'Give a man a fish and he will eat for a day. Teach him how to fish, and he will sit in a boat and drink beer all day.',
'name':'Anonymous',
},
{
'quote':'There are more old drunks than old doctors.',
'name':'Anonymous',
},
{
'quote':'A good local pub has much in common with a church, except that a pub is warmer, and there\'s more conversation.',
'name':'Anonymous',
},
{
'quote':'They who drink beer will think beer.',
'name':'Washington Irving',
},
{
'quote':'All right, brain, I don\'t like you and you don\'t like me - so let\'s just do this and I\'ll get back to killing you with beer.',
'name':'Homer Simpson',
},
{
'quote':'When I heated my home with oil, I used an average of 800 gallons a year. I have found that I can keep comfortably warm for an entire winter with slightly over half that quantity of beer.',
'name':'Dave Barry',
},
]


def get_quote():
    return random.choice(beer_quotes)

