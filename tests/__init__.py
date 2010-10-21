from twiggy.message import Message
import twiggy

def make_mesg():
    return Message(twiggy.levels.DEBUG,
                   "Hello {0} {who}",
                   {'shirt':42, 'name': 'jose'},
                   Message._default_options,
                   args=["Mister"],
                   kwargs={'who':"Funnypants"},
                   )
