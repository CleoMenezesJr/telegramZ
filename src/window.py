# window.py
#
# Copyright 2022 Cleo Menezes Jr.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk, WebKit2
import logging


@Gtk.Template(resource_path="/io/github/cleomenezesjr/telegramZ/window.ui")
class TelegramzWindow(Gtk.ApplicationWindow):
    __gtype_name__ = "TelegramzWindow"

    srch_entry = Gtk.Template.Child()
    btn_menu = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.web_view = WebKit2.WebView()
        self.web_view.load_uri("http://webz.dev")

        self.set_child(self.web_view)
        self.btn_menu.connect("clicked", self.on_menu_button)
        self.web_view.connect("load-changed", self.set_style)
        self.srch_entry.connect("activate", self.on_search)
        self.web_view.connect("permission-request", self._permission)

    def on_menu_button(self, status):
        self.web_view.run_javascript(
            # for some reason, using variables brake everything
            """
            if (document.querySelector("[title='Go back']")) {
                document.querySelector("[title='Go back']").click()
            } else if (document.querySelector("[title='Return to chat list']")) {
                document.querySelector("[title='Return to chat list']").click()
            } else {
                document.querySelector(".ripple-container").click()
            }
            """
        )

    def on_search(self, status):
        self.web_view.run_javascript(
            """
            if (document.activeElement.className != 'form-control')
              document.getElementById('telegram-search-input').focus();
            """
        )

    def set_style(self, view, event):
        if event == WebKit2.LoadEvent.FINISHED:
            self.web_view.run_javascript(
                """
                alert(navigator.userAgent)
                setTimeout(setStyle, 100);
                    function setStyle() {
                        let style = document.createElement('style');
                        style.type = 'text/css';
                        style.innerHTML = `
                            .bubble.menu-container {
                                margin-top: 15px !important;
                                margin-left: -8px !important;
                            }
                            #LeftMainHeader {
                                margin-top: -4rem !important;
                            }
                        `
                        document.head.appendChild(style);
                    }
                """
            )

    def _permission(self, webview: object, request: object):
        """Grant permission for notifications."""
        logging.info(f"PERMISSION: {request}")
        if type(request) == WebKit2.NotificationPermissionRequest:
            request.allow()
