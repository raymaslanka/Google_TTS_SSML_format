##########
#
# Google TTS SSML input check
#
# script checks a string input and verifies some SSML elements supported by Google's Cloud Text-to-Speech are formatted correctly
#
# Google's Cloud Text-to-Speech service does not support all SSML elements
# this script does not check all of Googles's Cloud Text-to-Speech service supported elements
#
##########

from lxml import etree

ssml_string = '<speak><emphasis level="strong">To be</emphasis><break time="220ms"/> or not to be, <break time="1000ms"/><emphasis level="moderate">that</emphasis>is the question.<break time="400ms"/> Whether ‘tis nobler in the mind to suffer The slings and arrows of outrageous fortune,<break time="200ms"/> Or to take arms against a sea of troubles  And by opposing end them.</speak>'

def check_Google_TTS_SSML_format(ssml_string):
    try:
        root = etree.fromstring(ssml_string, etree.XMLParser(resolve_entities=False))
        for element in root.iter():
            # print(element.tag)
            if element.tag == "break":
                if "time" not in element.attrib:
                    print("Invalid SSML: <break> tag is missing 'time' attribute.")
                    return False
                else:
                    time_value = element.get("time")
                    try:
                        float(time_value[:-2])
                        if time_value[-2:] not in ["ms", "s"]:
                            print(f"Invalid SSML: <break> tag has invalid time value '{time_value}'")
                            return False
                    except ValueError:
                        print(f"Invalid SSML: <break> tag has invalid time value '{time_value}'")
                        return False
            if element.tag == "emphasis":
                if "level" not in element.attrib:
                    print("Invalid SSML: <emphasis> tag is missing 'level' attribute.")
                    return False
                else:
                    level_value = element.get("level")
                    if level_value not in ["strong", "moderate", "reduced", "none"]:
                        print(f"Invalid SSML: <emphasis> tag has invalid level value '{level_value}'")
                        return False
            if element.tag == "say-as":
                if "interpret-as" not in element.attrib:
                    print("Invalid SSML: <say-as> tag is missing 'interpret-as' attribute.")
                    return False
                else:
                    interpret_as_value = element.get("interpret-as")
                    if interpret_as_value not in ["date", "time", "telephone", "cardinal", "ordinal", "digits", "fraction", "unit", "verbatim", "spell-out","currency"]:
                        print(f"Invalid SSML: <say-as> tag has invalid 'interpret-as' value '{interpret_as_value}'")
                        return False

        print("Valid SSML")
        return True
    except etree.XMLSyntaxError as e:
        print("Invalid SSML:", e)
        return False

if __name__ == "__main__":
    print(check_Google_TTS_SSML_format(ssml_string))

