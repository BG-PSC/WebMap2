import webbrowser

import flet as ft
import flet.map as map
import random
import os

import requests


class PointButton(ft.TextButton):
    def __init__(self, page: ft.Page, lines):
        super().__init__()


class MapFrame(ft.Container):
    def __init__(self, page: ft.Page, lines, kody):
        super().__init__()

        self.lines = lines
        self.kody = kody

        self.expand = 1
        self.border_radius = ft.border_radius.all(10)
        self.bgcolor = ft.Colors.WHITE
        # self.col=12

        marker_layer_ref = ft.Ref[map.MarkerLayer]()
        self.circle_layer_ref = ft.Ref[map.CircleLayer]()
        self.label_ref = ft.Ref[map.MarkerLayer]()
        self.label_ref_plots = ft.Ref[map.MarkerLayer]()
        self.lr_ref = ft.Ref[map.PolylineLayer]()
        self.plot_ref = ft.Ref[map.PolylineLayer]()

        self.main_map = map.Map(
            layers=[
                map.MarkerLayer(ref=self.label_ref, markers=[]),
                map.CircleLayer(ref=self.circle_layer_ref, circles=[]),
                map.PolylineLayer(ref=self.lr_ref, polylines=[]),
                map.PolylineLayer(ref=self.plot_ref, polylines=[]),
            ]
        )

        def handle_tap(e: map.MapTapEvent):

            if e.name == "tap":
                # webbrowser.open("https://bitly.com/")

                self.pkt = e.coordinates

                """marker_layer_ref.current.markers.clear()
                marker_layer_ref.current.markers.append(
                        map.Marker(
                            content=ft.Icon(
                                ft.Icons.LOCATION_ON, color=ft.cupertino_colors.DESTRUCTIVE_RED
                            ),
                            coordinates=e.coordinates,
                        )
                    )"""

            # webbrowser.open(f"https://www.google.pl/maps/place/{e.coordinates.latitude:.5f},{e.coordinates.longitude:.5f}")
            page.update()

        def handle_event(e: map.MapEvent):
            pass

        label = ft.Container(
            content=ft.Row(
                [
                    ft.Text(
                        "Click anywhere to add a Marker, right-click to add a CircleMarker."
                    )
                ]
            ),
            border_radius=ft.border_radius.all(10),
            bgcolor=ft.Colors.with_opacity(0.6, ft.Colors.PRIMARY_CONTAINER),
            padding=5,
            blur=15,
        )

        self.main_map = map.Map(
            expand=True,
            initial_center=map.MapLatitudeLongitude(51.1649819320, 21.6383970534),
            initial_zoom=12,
            min_zoom=10,
            max_zoom=21,
            interaction_configuration=map.MapInteractionConfiguration(
                flags=map.MapInteractiveFlag.ALL
            ),
            # on_init=lambda e: print(f"Initialized Map"),
            on_tap=lambda e: handle_tap(e),
            on_secondary_tap=lambda e: handle_tap(e),
            on_long_press=lambda e: handle_tap(e),
            # on_event=lambda e: print(e),
            layers=[
                map.TileLayer(
                    url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
                    # url_template="https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}"
                ),
                map.TileLayer(
                    # url_template="https://mt1.google.com/vt/lyrs=s&hl=pl&x={x}&y={y}&z={z}",
                    # url_template="./{z}/{x}/{y}.jpg",
                    # url_template="https://raw.githack.com/Rzezimioszek/WebMapTest/main/{z}/{x}/{y}.png",
                    # url_template="https://raw.githack.com/Rzezimioszek/WebMapTest/main/{z}/{x}/{y}.jpg",
                    # url_template="https://raw.githack.com/Rzezimioszek/Files/main/ortofotomapa/S17K/{z}/{x}/{y}.jpg",
                    url_template="https://raw.githubusercontent.com/BG-PSC/Files/refs/heads/main/ortofotomapa/lipsko/{z}/{x}/{y}.png",
                    # url_template="http://mapy.geoportal.gov.pl/wss/service/PZGIK/ORTO/WMTS/HighResolution?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=ORTOFOTOMAPA&STYLE=default&FORMAT=image%2Fjpeg&TILEMATRIXSET=EPSG%3A4326&TILEMATRIX=EPSG%3A4326%3A{z}&TILEROW={x}&TILECOL={y}"
                    # url_template="https://mapy.geoportal.gov.pl/wss/ext/OSM/BaseMap/tms/1.0.0/osm_3857/GLOBAL_WEBMERCATOR/{z}/{x}/{y}.png",
                    # url_template="https://raw.githack.com/Rzezimioszek/Files/main/ortofotomapa/S17K2/{z}/{x}/{y}.jpg",
                    # on_image_error=lambda e: print("TileLayer Error"),
                    pan_buffer=1,
                ),
                map.PolylineLayer(ref=self.lr_ref, polylines=[]),
                map.MarkerLayer(
                    ref=self.label_ref_plots,
                    markers=[],
                ),
                map.MarkerLayer(
                    ref=self.label_ref,
                    markers=[],
                ),
                map.CircleLayer(
                    ref=self.circle_layer_ref,
                    circles=[],
                ),
                map.SimpleAttribution(
                    text="2025 BG-P.PL, OpenStreetMap contributors, ESRI World Imagery",
                    alignment=ft.alignment.bottom_left,
                ),
            ],
        )

        def elBtn_click(e):
            url = f"https://www.google.pl/maps/place/{self.pkt.latitude:.5f},{self.pkt.longitude:.5f}"
            try:
                webbrowser.open(url)
            except Exception as er:
                page.launch_url(url)

        elBtn = ft.ElevatedButton("Nawiguj", on_click=lambda e: elBtn_click(e))

        def listBtn_click(e):
            self.listControl.visible = not self.listControl.visible
            self.img_stack.visible = not self.img_stack.visible
            self.main_map.visible = not self.main_map.visible
            if listBtn.text == "🗺 Mapa":
                listBtn.text = "📷 Zdjęcia punktów granicznych"
                listBtn.tooltip = "Pokaż listę punktów"
                zoom_to_allBtn.visible = True
                self.switch_bcgBtn.visible = True

            else:
                listBtn.text = "🗺 Mapa"
                listBtn.tooltip = "Pokaż mapę"
                zoom_to_allBtn.visible = False
                self.switch_bcgBtn.visible = False
            page.update()
            self.zoom_to_all_objects()

        listBtn = ft.ElevatedButton(
            "📷 Zdjęcia punktów granicznych",
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.RED,
            on_click=lambda e: listBtn_click(e),
        )

        listBtn.tooltip = "Pokaż listę punktów"

        zoom_to_allBtn = ft.ElevatedButton(
            "Pokaż całą mapę",
            on_click=lambda e: self.main_map.move_to(
                map.MapLatitudeLongitude(51.1649819320, 21.6383970534), 12
            ),
        )

        self.switch_bcgBtn = ft.ElevatedButton("SATELITA 🛰", on_click=self.switch_bcg)

        self.listControl = ft.ListView(expand=1, spacing=5, padding=5)
        # self.listControl.visible = False

        self.image_file = ft.Image(  # expand=1,
            src="https://raw.githubusercontent.com/BG-PSC/Files/main/ortofotomapa/S17K/18/147891/87921.jpg",
            fit=ft.ImageFit.FIT_HEIGHT,
            height=400,
        )

        self.image_label = ft.Text(
            "",
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.BLACK,
        )
        self.image_expand = ft.Text(
            "🔳 Powiększ / pobierz",
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.BLACK,
        )
        self.image_navigate = ft.Text(
            "🌐 Nawiguj", color=ft.Colors.WHITE, bgcolor=ft.Colors.BLACK
        )
        self.image_pin = "https://www.google.com/maps?q={},{}&label={}"
        self.img_stack = ft.Stack(
            controls=[
                self.image_file,
                ft.Container(
                    content=self.image_label,
                    bottom=55,
                    left=5,
                ),
                ft.Container(
                    content=self.image_expand,
                    on_click=lambda e: page.launch_url(self.image_file.src),
                    bottom=30,
                    left=5,
                ),
                ft.Container(
                    content=self.image_navigate,
                    on_click=lambda e: page.launch_url(self.image_pin),
                    bottom=5,
                    left=5,
                ),
            ],
        )

        # extras_row = ft.ResponsiveRow([self.listControl, self.image_stack])
        # extras_row.visible = False
        self.listControl.visible = False
        self.img_stack.visible = False

        self.add_plots()
        self.add_lr()
        self.add_labels()
        self.pb = ft.Row(
            [
                ft.ProgressRing(width=16, height=16, stroke_width=2),
                ft.Text("Ładowanie danych"),
            ]
        )
        self.pb.visible = False

        self.content = ft.Stack(
            controls=[
                ft.Column(
                    [
                        self.main_map,
                        self.img_stack,
                        self.listControl,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.END,
                ),
                ft.Column(
                    [
                        zoom_to_allBtn,
                        self.switch_bcgBtn,
                        listBtn,
                        # elBtn
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.END,
                    bottom=15,
                    right=5,
                ),
                ft.Column([self.pb], top=5, left=5),
            ],
            expand=1,
        )

    def switch_bcg(self, e=None):
        # Check the current map layer and toggle
        if hasattr(self, "current_layer") and self.current_layer == "esri":
            self.main_map.layers[0] = map.TileLayer(
                url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png"
            )
            self.current_layer = "osm"
            self.switch_bcgBtn.text = "🛰 SATELITA"
        else:
            self.main_map.layers[0] = map.TileLayer(
                url_template="https://services.arcgisonline.com/arcgis/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
            )
            self.current_layer = "esri"
            self.switch_bcgBtn.text = "🗺 MAPA"  #
        self.main_map.update()
        self.page.update()

    def clear_layers(self):
        self.circle_layer_ref.current.circles.clear()
        self.label_ref.current.markers.clear()
        print(
            f"Clearing layers: {len(self.circle_layer_ref.current.circles)}, {len(self.label_ref.current.markers)}"
        )
        self.main_map.update()

    def add_lr(self):

        file = requests.get("https://bg-psc.github.io/Files/pliki/sztabin/lr.txt").text
        lines = str(file).split("\n")

        current = ""
        temp_l = []
        lrs = []

        for line in lines:
            temp = line.split("\t")
            if current == "":
                current = temp[0]
            if current == temp[0]:
                temp_l.append(map.MapLatitudeLongitude(float(temp[3]), float(temp[2])))
            else:
                if len(temp_l) > 0:
                    lrs.append(temp_l.copy())
                    temp_l.clear()
                current = temp[0]
                temp_l.append(map.MapLatitudeLongitude(float(temp[3]), float(temp[2])))
        lrs.append(temp_l)

        # print(lrs)

        i = 0

        for lr in lrs:
            i += 1
            # print(i, lr)
            self.lr_ref.current.polylines.append(
                map.PolylineMarker(
                    border_stroke_width=2,
                    border_color=ft.Colors.RED,
                    color=ft.Colors.RED,
                    coordinates=[*lr],
                )
            )

    def add_label(self, text, lat, lon):

        new_marker = map.Marker(
            content=ft.Stack(
                [
                    ft.Text(
                        spans=[
                            ft.TextSpan(
                                f"{text}",
                                ft.TextStyle(
                                    size=10,
                                    weight=ft.FontWeight.BOLD,
                                    foreground=ft.Paint(
                                        color=ft.Colors.WHITE,
                                        stroke_width=2,
                                        stroke_join=ft.StrokeJoin.ROUND,
                                        style=ft.PaintingStyle.STROKE,
                                    ),
                                ),
                            ),
                        ],
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        value=f"{text}",
                        color=ft.Colors.BLUE,
                        size=10,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.LEFT,
                    ),
                ],
            ),
            alignment=ft.alignment.center,
            width=70,
            coordinates=map.MapLatitudeLongitude(lat, lon),
        )
        self.label_ref_plots.current.markers.append(new_marker)
        # self.page.update()

    def add_labels(self):
        file = requests.get(
            "https://bg-psc.github.io/Files/pliki/sztabin/etykiety.txt"
        ).text
        lines = str(file).split("\n")

        for punkt in lines:
            punkt = punkt.split()
            self.add_label(punkt[0], float(punkt[2]), float(punkt[1]))

    def add_plots(self):

        file = requests.get(
            "https://bg-psc.github.io/Files/pliki/sztabin/dzialki.txt"
        ).text
        lines = str(file).split("\n")

        current = ""
        temp_l = []
        lrs = []

        for line in lines:
            temp = line.split("\t")
            if current == "":
                current = temp[0]

            if current == temp[0]:
                print(temp)
                temp_l.append(map.MapLatitudeLongitude(float(temp[3]), float(temp[2])))
            else:
                if len(temp_l) > 0:
                    lrs.append(temp_l.copy())
                    temp_l.clear()
                current = temp[0]
                temp_l.append(map.MapLatitudeLongitude(float(temp[3]), float(temp[2])))
        lrs.append(temp_l)

        # print(lrs)

        i = 0

        for lr in lrs:
            i += 1
            # print(i, lr)
            self.lr_ref.current.polylines.append(
                map.PolylineMarker(
                    border_stroke_width=0.5,
                    border_color=ft.Colors.BLUE,
                    color=ft.Colors.BLUE,
                    coordinates=[*lr],
                )
            )

    def add_circle(self, name_tag, lat, lon):

        new_marker = map.Marker(
            content=ft.Stack(
                [
                    ft.Text(
                        spans=[
                            ft.TextSpan(
                                f"{name_tag}",
                                ft.TextStyle(
                                    size=12,
                                    weight=ft.FontWeight.BOLD,
                                    foreground=ft.Paint(
                                        color=ft.Colors.BLACK,
                                        stroke_width=2,
                                        stroke_join=ft.StrokeJoin.ROUND,
                                        style=ft.PaintingStyle.STROKE,
                                    ),
                                ),
                            ),
                        ],
                        text_align=ft.TextAlign.LEFT,
                    ),
                    ft.Text(
                        value=f"{name_tag}",
                        # bgcolor=ft.colors.with_opacity(0.2, ft.colors.WHITE),
                        color=ft.Colors.WHITE,
                        size=12,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.LEFT,
                    ),
                ],
            ),
            alignment=ft.alignment.top_center,
            width=70,
            coordinates=map.MapLatitudeLongitude(lat, lon),
        )

        self.label_ref.current.markers.append(new_marker)

        self.circle_layer_ref.current.circles.append(
            map.CircleMarker(
                radius=3,
                coordinates=map.MapLatitudeLongitude(lat, lon),
                color=ft.Colors.RED,
                border_color=ft.Colors.WHITE,
                border_stroke_width=1,
            )
        )

        self.page.update()

    def point_zoom(self, e):

        spl = str(e.control.text).split()
        try:
            image_url = f"https://raw.githubusercontent.com/BG-PSC/Files/main/pliki/graniczniki_lipsko/{spl[2]}.jpg"
            response = requests.head(image_url)
            if response.status_code == 200:
                self.image_file.src = image_url
            else:
                self.image_file.src = "https://raw.githubusercontent.com/BG-PSC/Files/main/pliki/placeholder.jpg"
            self.image_label.value = f"📍 {spl[2]}"
            self.image_pin = (
                f"https://www.google.com/maps?q={spl[4]},{spl[6]}&label={spl[2]}"
            )
            print(spl)
        except Exception as e:
            print(spl)
            self.image_file.src = "https://raw.githubusercontent.com/BG-PSC/Files/main/pliki/placeholder.jpg"
            self.image_label.value = ""
            print(e)

        self.page.update()

    def load_values(self, value):
        value = value.upper()
        self.clear_layers()
        self.listControl.controls.clear()
        self.pb.visible = True

        btn = dict()

        i = 0
        seen_points = set()  # zbiór unikalnych punktów
        #
        lines = []
        plot = ""

        if value == "ALL":
            for line in self.lines:
                spl = line.split("\t")
                lat, lon = float(spl[-1]), float(spl[-2])
                name_tag = f"{spl[-3]}"

                if (lat, lon) in seen_points:
                    continue

                seen_points.add((lat, lon))

                str_btn = (
                    f"Numer punktu: {spl[-3]}    B: {spl[-1]}     L: {spl[-2]}".replace(
                        "\r", ""
                    )
                )
                btn[i] = ft.ElevatedButton(
                    str_btn, on_click=lambda e: self.point_zoom(e)
                )

                self.listControl.controls.append(btn[i])
                self.add_circle(name_tag, float(spl[-1]), float(spl[-2]))
                i += 1

            self.pb.visible = False
            self.page.update()
            return

        for kod in self.kody:

            if value == kod.split("\t")[0]:  # change
                plot = kod.split("\t")[-1]

                for line in self.lines:

                    spl = line.split("\t")
                    lat, lon = float(spl[-1]), float(spl[-2])
                    name_tag = f"{spl[-3]}"

                    if (lat, lon) in seen_points:
                        continue

                    if spl[0] == plot:
                        seen_points.add((lat, lon))

                        str_btn = f"Numer punktu: {spl[-3]}    B: {spl[-1]}     L: {spl[-2]}".replace(
                            "\r", ""
                        )
                        btn[i] = ft.ElevatedButton(
                            str_btn, on_click=lambda e: self.point_zoom(e)
                        )

                        self.listControl.controls.append(btn[i])
                        self.add_circle(name_tag, float(spl[-1]), float(spl[-2]))
                        i += 1
        self.pb.visible = False
        self.zoom_to_all_objects()
        self.page.update()

    def zoom_to_all_objects(self):
        if not self.circle_layer_ref.current.circles:
            return  # Jeśli brak okręgów, nie rób nic

        latitudes = [
            circle.coordinates.latitude
            for circle in self.circle_layer_ref.current.circles
        ]
        longitudes = [
            circle.coordinates.longitude
            for circle in self.circle_layer_ref.current.circles
        ]

        if not latitudes or not longitudes:
            return

        # Oblicz bounding box (zakres widocznych punktów)
        min_lat, max_lat = min(latitudes), max(latitudes)
        min_lon, max_lon = min(longitudes), max(longitudes)

        # Środek widoku
        center_lat = (min_lat + max_lat) / 2
        center_lon = (min_lon + max_lon) / 2

        # Określenie optymalnego zoomu
        lat_diff = max_lat - min_lat
        lon_diff = max_lon - min_lon
        max_diff = max(lat_diff, lon_diff)

        if max_diff < 0.001:
            zoom = 18  # Bardzo blisko
        elif max_diff < 0.01:
            zoom = 17
        elif max_diff < 0.05:
            zoom = 15
        elif max_diff < 0.1:
            zoom = 14
        else:
            zoom = max(12, 15 - max_diff * 30)  # Dynamiczny zoom

        # Przeniesienie mapy
        self.main_map.move_to(
            destination=map.MapLatitudeLongitude(center_lat, center_lon), zoom=int(zoom)
        )

        self.page.update()


def main(page: ft.Page):
    debug = False

    file = requests.get(
        "https://raw.githubusercontent.com/BG-PSC/Files/main/pliki/sztabin/punkty.txt"
    ).text
    # file = requests.get("https://bg-psc.github.io/Files/pliki/punkty.txt").text
    lines = str(file).split("\n")
    lines = [line.strip() for line in lines if line.strip()]
    # file = requests.get("https://bg-psc.github.io/Files/pliki/kod-dzialka.txt").text
    file = requests.get(
        "https://raw.githubusercontent.com/BG-PSC/Files/main/pliki/sztabin/kod-dzialka.txt"
    ).text
    kody = str(file).split("\n")
    kody = [kod.strip() for kod in kody if kod.strip()]

    if debug:
        with open(r"D:\Python\kuba\web_map\Files\pliki\punkty.txt", "r") as file:
            lines = file.read().splitlines()

        with open(r"D:\Python\kuba\web_map\Files\pliki\kod-dzialka.txt", "r") as file:
            kody = file.read().splitlines()

    # main_row.controls.append(label)

    mf = MapFrame(page, lines, kody)

    def submit_on_clik(e):
        # mf.visible = not mf.visible
        mf.clear_layers()
        page.update()
        # query.value
        mf.load_values(query.value)

    query = ft.TextField(
        label="Wprowadź kod otrzymany w zawiadomieniu",
        on_submit=lambda e: submit_on_clik(e),
        height=50,
        col={"xs": 4, "sm": 4, "md": 3},
    )
    submit = ft.ElevatedButton(
        "Zatwierdź",
        on_click=lambda e: submit_on_clik(e),
        height=50,
        bgcolor=ft.Colors.PRIMARY,
        color=ft.Colors.ON_PRIMARY,
        col={"xs": 3, "sm": 3, "md": 1},
    )

    logo = ft.GestureDetector(
        content=ft.Image(
            src="https://raw.githubusercontent.com/BG-PSC/WebMap/main/assets/logo.png",
            width=50,
            height=50,
            fit=ft.ImageFit.CONTAIN,
        ),
        on_tap=lambda e: page.launch_url("https://bg-p.pl"),
        mouse_cursor=ft.MouseCursor.CLICK,
        col={"xs": 1, "sm": 1, "md": 1},
    )

    aboutBtn = ft.ElevatedButton(
        content=ft.Row(
            controls=[
                ft.Image(
                    src="https://raw.githubusercontent.com/BG-PSC/WebMap/refs/heads/main/assets/gddkia.png",
                    width=40,
                    height=40,
                ),
                ft.Text("O inwestycji", color=ft.Colors.DEEP_ORANGE),
            ]
        ),
        on_click=lambda e: page.launch_url("https://www.dk79-obwodnicalipska.pl/"),
        col={"xs": 3, "sm": 3, "md": 1.5},
        height=50,
    )

    main_row = ft.ResponsiveRow(
        controls=[logo, query, submit, aboutBtn],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.START,
    )

    page.add(main_row)

    page.add(mf)

    page.theme_mode = ft.ThemeMode.LIGHT

    page.update()


if __name__ == "__main__":
    site = ft.app(main, view=ft.AppView.WEB_BROWSER)
