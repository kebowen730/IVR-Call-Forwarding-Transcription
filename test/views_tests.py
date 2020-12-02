import xml.etree.ElementTree as ElementTree
from twilio.rest import Client

from .base import BaseTestCase
from flask import url_for
from unittest.mock import patch

class ViewsTests(BaseTestCase):
    
    def test_index_should_render_default_view(self):
        self.client.get('/')

        self.assert_template_used('index.html')


    def test_post_to_welcome_should_serve_twiml(self):
        response = self.client.post('/ivr/welcome')
        twiml = ElementTree.fromstring(response.data)

        assert not twiml.findall("./Gather/Say") == []
        assert twiml.findall("./Gather")[0].attrib["action"] == url_for('menu')


    def test_post_to_menu_with_digit_1_should_serve_twiml_with_dial_and_hangup(self):
        response = self.client.post('/ivr/menu', data=dict(Digits="1"), follow_redirects=True)
        twiml = ElementTree.fromstring(response.data)

        assert len(twiml.findall("./Dial")) == 1


    def test_post_to_menu_with_digit_2_should_serve_twiml_with_dial_and_hangup(self):
        response = self.client.post('/ivr/menu', data=dict(Digits="2"), follow_redirects=True)
        twiml = ElementTree.fromstring(response.data)

        assert len(twiml.findall("./Dial")) == 1


    def test_post_to_menu_with_digit_3_should_serve_twiml_with_redirect_to_finance_voicemail(self):
        response = self.client.post('/ivr/menu', data=dict(Digits="3"), follow_redirects=True)
        twiml = ElementTree.fromstring(response.data)

        assert not twiml.findall("./Redirect") == []
        assert twiml.findall("./Redirect")[0].text == url_for('finance_voicemail')


    def test_post_to_menu_with_digit_4_should_serve_twiml_with_redirect_to_work_voicemail(self):
        response = self.client.post('/ivr/menu', data=dict(Digits="4"), follow_redirects=True)
        twiml = ElementTree.fromstring(response.data)

        assert not twiml.findall("./Redirect") == []
        assert twiml.findall("./Redirect")[0].text == url_for('work_voicemail')
        

    def test_post_to_menu_with_digit_5_should_serve_twiml_with_redirect_to_misc_voicemail(self):
        response = self.client.post('/ivr/menu', data=dict(Digits="5"), follow_redirects=True)
        twiml = ElementTree.fromstring(response.data)

        assert not twiml.findall("./Redirect") == []
        assert twiml.findall("./Redirect")[0].text == url_for('misc_voicemail')


    def test_post_to_menu_with_digit_6_should_redirect_to_welcome(self):
        response = self.client.post('/ivr/menu', data=dict(Digits="6"), follow_redirects=True)
        twiml = ElementTree.fromstring(response.data)

        assert not twiml.findall("./Redirect") == []
        assert twiml.findall("./Redirect")[0].text == url_for('welcome')


    def test_post_to_menu_with_digit_out_of_range_should_redirect_to_welcome(self):
        response = self.client.post('/ivr/menu', data=dict(Digits="7"), follow_redirects=True)
        twiml = ElementTree.fromstring(response.data)

        assert not twiml.findall("./Redirect") == []
        assert twiml.findall("./Redirect")[0].text == url_for('welcome')    
