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


@Gtk.Template(resource_path='/io/github/cleomenezesjr/telegramZ/window.ui')
class TelegramzWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'TelegramzWindow'

    btn_menu = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.web_view = WebKit2.WebView()
        self.web_view.load_uri("http://webz.dev")
        self.web_view.run_javascript(
            """
            "Object.defineProperty(navigator, 'userAgent', {
                get: function () {
                    return '"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15"';
                }
            });"
            """
        )

        self.set_child(self.web_view)
        self.btn_menu.connect("clicked", self.on_reload_button_clicked)
        self.web_view.connect("load-changed", self.say)

    def on_reload_button_clicked(self, status):
        self.web_view.run_javascript(
            """
            document.querySelector(".ripple-container").click()
            """
        )

    def say(self, view, event):
        if event == WebKit2.LoadEvent.FINISHED:
            self.web_view.run_javascript(
                """
                const myTimeout = setTimeout(setStyle, 100);
                    function setStyle() {
                        let style = document.createElement('style');
                        style.type = 'text/css';
                        style.innerHTML = `
                            .Button.smaller.translucent.round.has-ripple {
                                    display: none !important;
                                }
                            .SearchInput {
                                margin-left: auto !important;
                                max-width: initial !important;
                            }
                            .bubble.menu-container {
                                margin-top: -30px !important;
                                margin-left: -8px !important;
                            }


                        `
                        document.head.appendChild(style);
                    }
                """
            )

