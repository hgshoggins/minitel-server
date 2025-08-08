"""
Created on 03 Jun 2021

@author: hgshoggins
"""
from minitel_server.page import DefaultPageHandler, PageContext, \
    Page
import logging
from minitel_server.terminal import Terminal
from minitel_server.exceptions import UserTerminateSessionError, MinitelTimeoutError
import datetime
import urllib.request

logger = logging.getLogger('CO2')


class HandlerCo2(DefaultPageHandler):
    """
    classdocs
    """

    def __init__(self, minitel, context):
        """
        Constructor
        """
        super().__init__(minitel, context)
        logger.info('in our custom handler')

    def after_rendering(self):
        logger.debug('In after_rendering callback')
        while True:
            try:
                today = urllib.request.urlopen('https://co2.apps.les-ateliers.co/?minitel=1&sensor=1').read().decode('utf-8')
                self.minitel.move_cursor(12, 9)
                self.minitel.double_size()
                self.minitel.print_text(today + ' ppm')
                self.minitel.clear_eol()
                self.minitel.normal_size()
                self.minitel.move_cursor(15, 11)
                self.minitel.print_text(datetime.datetime.now().strftime('%H:%M:%S'))
                self.minitel.clear_eol()

                # Waits for a key press (the form is empty)
                key = self.minitel.wait_form_inputs(1)
                if key == Terminal.RETOUR:
                    next_page = Page.get_page(self.context.current_page.service, None)
                    return PageContext(self, next_page)
                if key == Terminal.CONNEXION_FIN:
                    logger.debug("Connection/fin from {}".format(self.context.current_page.fullname))
                    raise UserTerminateSessionError
            except MinitelTimeoutError:
                pass
        return None
