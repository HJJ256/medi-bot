from rasa.nlu.components import Component
import typing
from typing import Any, Optional, Text, Dict
# import enchant,difflib
import string
# from spellchecker import SpellChecker
# spell = SpellChecker()
import re
from collections import Counter
from emoji import UNICODE_EMOJI

if typing.TYPE_CHECKING:
    from rasa.nlu.model import Metadata


class SpellChecker(Component):
    """A new component"""

    # Defines what attributes the pipeline component will
    # provide when called. The listed attributes
    # should be set by the component on the message object
    # during test and train, e.g.
    # ```message.set("entities", [...])```
    provides = ['text'] #set as text but shouldn't really have much influence on the component

    # Which attributes on a message are required by this
    # component. e.g. if requires contains "tokens", than a
    # previous component in the pipeline needs to have "tokens"
    # within the above described `provides` property.
    requires = []

    # Defines the default configuration parameters of a component
    # these values can be overwritten in the pipeline configuration
    # of the model. The component should choose sensible defaults
    # and should be able to create reasonable results with the defaults.
    defaults = {}

    # Defines what language(s) this component can handle.
    # This attribute is designed for instance method: `can_handle_language`.
    # Default value is None which means it can handle all languages.
    # This is an important feature for backwards compatibility of components.
    language_list = None

    def __init__(self, component_config=None):
        super(SpellChecker, self).__init__(component_config)

    def train(self, training_data, cfg, **kwargs):
        """Train this component.

        This is the components chance to train itself provided
        with the training data. The component can rely on
        any context attribute to be present, that gets created
        by a call to :meth:`components.Component.pipeline_init`
        of ANY component and
        on any context attributes created by a call to
        :meth:`components.Component.train`
        of components previous to this one."""
        pass
    def process(self, message, **kwargs):
        """Process an incoming message.

        This is the components chance to process an incoming
        message. The component can rely on
        any context attribute to be present, that gets created
        by a call to :meth:`components.Component.pipeline_init`
        of ANY component and
        on any context attributes created by a call to
        :meth:`components.Component.process`
        of components previous to this one."""
      
        def load_custom_dictionary(text):
            return re.findall(r'\w+', text.lower())
        WORDS = Counter(load_custom_dictionary(open('./chatbot_vocab.txt').read()))
        def word_probablity(word, N=sum(WORDS.values())): 
            "Probability of `word`."
            return WORDS[word] / N
        def correction(word): 
            "Most probable spelling correction for word  wrt to custom dictionary "
            return max(possible_candidates(word), key=word_probablity)
        def possible_candidates(word): 
            "Generate possible spelling corrections for given word."
            return (known([word]) or known(edits1(word)) or known(edits2(word)) or 
                [word])
        def known(words): 
            "The subset of `words` that appear in the dictionary of WORDS."
            return set(w for w in words if w in WORDS)
        def edits1(word):
            "All edits that are one edit away from `word`."
            letters    = 'abcdefghijklmnopqrstuvwxyz'
            splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
            deletes    = [L + R[1:]               for L, R in splits if R]
            transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
            replaces   = [L + c + R[1:]           for L, R in splits if R for c in 
                        letters]
            inserts    = [L + c + R               for L, R in splits for c in 
            letters]
            return set(deletes + transposes + replaces + inserts)
        def edits2(word): 
            "All edits that are two edits away from `word`."
            return (e2 for e1 in edits1(word) for e2 in edits1(e1))
        def is_emoji(s):
            return s in UNICODE_EMOJI

        sentence = message.text 
        string_split = sentence.split()
        new_string = []
        for i in string_split:
            if is_emoji(i):
                word = UNICODE_EMOJI[i]
                word = " ".join(word.split(":")[1].split("_"))
                new_string.append(word)
            else:
                new_string.append(i)

        new_sentence = " ".join(new_string)
        listofsentences = new_sentence.lower().split()
        actual_message = []
        for i in listofsentences:
            actual_message.append(correction(i))
        mesg = " ".join(actual_message)  
        print(mesg)          
        message.text = mesg #set the corrected message as the message for the next components to process

    def persist(self, file_name: Text, model_dir: Text) -> Optional[Dict[Text, Any]]:
        """Persist this component to disk for future loading."""

        pass

    @classmethod
    def load(
        cls,
        meta: Dict[Text, Any],
        model_dir: Optional[Text] = None,
        model_metadata: Optional["Metadata"] = None,
        cached_component: Optional["Component"] = None,
        **kwargs: Any
    ) -> "Component":
        """Load this component from file."""

        if cached_component:
            return cached_component
        else:
            return cls(meta)