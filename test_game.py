# import unittest
import pytest
from unittest.mock import patch, Mock

def test_players:
    

# mocking raw input
# https://stackoverflow.com/questions/21046717/python-mocking-raw-input-in-unittests

# def test_enigma_encipher(enigma):
    # # check bad input
    # with pytest.raises(ValueError):
    #     enigma.encipher('?')

    # # check bad input 2
    # with pytest.raises(TypeError):
    #     enigma.encipher(100)

    # assert enigma.encipher("CHILL") == "QUPCN"
    # assert enigma.encipher("c  h i ll") == "HRKPO"
    # assert enigma.encipher("") == ""

    # with patching
    # with patch.object(enigma, "encode_decode_letter") as edl:
    #     edl.return_value = "x"

    #     assert enigma.encipher("") == ""
    #     edl.assert_not_called()

    #     assert enigma.encipher(" h ") == "x"
    #     edl.assert_called_with("H")