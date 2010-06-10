from twiggy.Message import Message
import twiggy

def make_mesg():
    return Message(twiggy.Levels.DEBUG,
                   "Hello {0} {who}",
                   {'shirt':42, 'name': 'jose'},
                   Message._default_options,
                   "Mister",
                   who="Funnypants",
                   )
