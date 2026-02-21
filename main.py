"""
周易学习程序 - 主应用
使用Flet框架构建交互式周易学习工具
"""

import flet as ft
from gua_data import (
    ALL_GUAS,
    search_gua,
    get_gua_by_index,
    get_gua_by_numbers,
    binary_to_gua,
    YaoType,
    Yao,
    Gua,
    TRIGRAMS,
    init_data,
)
from typing import List, Optional

# 统一的爻线宽度 - 放大尺寸
YAO_LINE_WIDTH = 180  # 爻线本身宽度（从100放大到180）
YAO_TOTAL_WIDTH = 220  # 包含"变"字的总宽度（从140放大到220）


class YaoLineWidget(ft.Container):
    """爻线组件 - 统一处理阴阳爻的显示"""

    def __init__(self, yao: Yao, is_highlighted: bool = False):
        self.yao = yao
        self.is_highlighted = is_highlighted

        super().__init__(
            content=self._create_yao_line(),
            width=YAO_LINE_WIDTH,
            height=30,
            padding=ft.Padding(top=8, bottom=8, left=0, right=0),
            alignment=ft.Alignment(0, 0),
        )

    def _create_yao_line(self):
        """创建爻线"""
        # 高亮样式：红色、加粗
        color = ft.Colors.RED if self.is_highlighted else ft.Colors.BLACK
        height = 18 if self.is_highlighted else 14  # 高亮时更粗

        if self.yao.is_yang:
            # 阳爻 —— 一根完整的线
            return ft.Container(
                width=YAO_LINE_WIDTH,
                height=height,
                bgcolor=color,
                border_radius=9 if self.is_highlighted else 7,
            )
        else:
            # 阴爻 —— 两根比较短的线，中间断开
            gap = 16
            segment_width = (YAO_LINE_WIDTH - gap) // 2

            return ft.Row(
                [
                    ft.Container(
                        width=segment_width,
                        height=height,
                        bgcolor=color,
                        border_radius=9 if self.is_highlighted else 7,
                    ),
                    ft.Container(
                        width=gap,
                        height=height,
                        bgcolor=ft.Colors.TRANSPARENT,
                    ),
                    ft.Container(
                        width=segment_width,
                        height=height,
                        bgcolor=color,
                        border_radius=9 if self.is_highlighted else 7,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=0,
            )


class ClickableYaoLine(ft.Container):
    """可点击的爻组件 - 用于本卦区域"""

    def __init__(
        self,
        original_yao: Yao,
        display_yao: Yao,
        on_click=None,
        is_changing: bool = False,
        is_highlighted: bool = False,
    ):
        self.original_yao = original_yao
        self.display_yao = display_yao
        self.on_yao_click = on_click
        self.is_changing = is_changing
        self.is_highlighted = is_highlighted

        super().__init__(
            content=self._create_content(),
            on_click=self._handle_click,
            padding=0,
            width=YAO_TOTAL_WIDTH,
        )

    def _create_content(self):
        """创建爻的视觉内容"""
        # 爻线，支持高亮
        yao_line = YaoLineWidget(self.display_yao, is_highlighted=self.is_highlighted)

        # 创建行，包含爻线和标记（变/高亮）
        if self.is_changing and self.is_highlighted:
            # 同时是变爻和高亮
            return ft.Row(
                [
                    yao_line,
                    ft.Container(width=8),
                    ft.Container(
                        content=ft.Text(
                            "变★",
                            size=12,
                            color=ft.Colors.RED,
                            weight=ft.FontWeight.BOLD,
                        ),
                        width=36,
                        alignment=ft.Alignment(0, 0),
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=0,
            )
        elif self.is_changing:
            return ft.Row(
                [
                    yao_line,
                    ft.Container(width=8),
                    ft.Container(
                        content=ft.Text(
                            "变",
                            size=12,
                            color=ft.Colors.RED,
                            weight=ft.FontWeight.BOLD,
                        ),
                        width=24,
                        alignment=ft.Alignment(0, 0),
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=0,
            )
        elif self.is_highlighted:
            return ft.Row(
                [
                    yao_line,
                    ft.Container(width=8),
                    ft.Container(
                        content=ft.Text(
                            "★",
                            size=14,
                            color=ft.Colors.RED,
                            weight=ft.FontWeight.BOLD,
                        ),
                        width=24,
                        alignment=ft.Alignment(0, 0),
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=0,
            )
        else:
            return ft.Row(
                [
                    yao_line,
                    ft.Container(width=8),
                    ft.Container(width=24),  # 占位保持对齐
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=0,
            )

    def _handle_click(self, e):
        """处理点击事件"""
        if self.on_yao_click:
            self.on_yao_click(self.original_yao)


class InteractiveHexagramView(ft.Column):
    """可交互的卦象视图 - 包含卦辞和爻辞"""

    def __init__(
        self,
        original_gua: Gua,
        on_yao_click=None,
        title: str = "",
        changing_positions: Optional[List[int]] = None,
        highlighted_positions: Optional[List[int]] = None,
    ):
        self.original_gua = original_gua
        self.on_yao_click = on_yao_click
        self.title = title
        self.changing_positions = (
            changing_positions if changing_positions is not None else []
        )
        self.highlighted_positions = (
            highlighted_positions if highlighted_positions is not None else []
        )

        # 根据变爻状态确定当前显示的卦
        if self.changing_positions:
            self.display_gua = original_gua.get_changed_gua(self.changing_positions)
        else:
            self.display_gua = original_gua

        super().__init__(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        )

        self._build()

    def _build(self):
        """构建卦象视图"""
        self.controls = []

        # 标题
        if self.title:
            self.controls.append(
                ft.Text(self.title, size=24, weight=ft.FontWeight.BOLD)  # 从18放大到24
            )

        # 卦名信息
        trigram_names = {
            "qian": "天",
            "kun": "地",
            "zhen": "雷",
            "gen": "山",
            "kan": "水",
            "li": "火",
            "xun": "风",
            "dui": "泽",
        }
        upper = trigram_names.get(self.display_gua.upper_gua, "")
        lower = trigram_names.get(self.display_gua.lower_gua, "")

        self.controls.append(
            ft.Text(
                f"{self.display_gua.name} ({upper}{lower}{self.display_gua.name})",
                size=28,  # 从20放大到28
                weight=ft.FontWeight.BOLD,
            )
        )

        # 卦辞（使用display_gua的卦辞）
        self.controls.append(
            ft.Container(
                content=ft.Text(
                    f"卦辞：{self.display_gua.description}",
                    size=16,  # 从14放大到16
                    color=ft.Colors.GREY_800,
                ),
                padding=15,  # 从10放大到15
                bgcolor=ft.Colors.GREY_100,
                border_radius=5,
                width=600,  # 从500放大到600
            )
        )

        # 分隔线
        self.controls.append(ft.Divider())

        # 六爻（从上往下显示）
        # 注意：使用display_gua的爻来显示，但保留original_gua的爻用于点击
        original_yaos_dict = {y.position: y for y in self.original_gua.yaos}

        for i, display_yao in enumerate(reversed(self.display_gua.yaos)):
            position = display_yao.position
            original_yao = original_yaos_dict[position]
            is_changing = position in self.changing_positions
            is_highlighted = position in self.highlighted_positions

            yao_line = ClickableYaoLine(
                original_yao=original_yao,
                display_yao=display_yao,
                on_click=self.on_yao_click,
                is_changing=is_changing,
                is_highlighted=is_highlighted,
            )

            # 爻位标签
            position_labels = ["上爻", "五爻", "四爻", "三爻", "二爻", "初爻"]
            label = position_labels[i]

            # 爻辞和小象传（使用display_gua的爻辞）
            yao_text = display_yao.text
            xiang_text = display_yao.xiang

            # 高亮时的样式
            text_color = ft.Colors.RED if is_highlighted else ft.Colors.GREY_700
            text_weight = ft.FontWeight.BOLD if is_highlighted else ft.FontWeight.NORMAL

            row = ft.Row(
                [
                    # 爻位标签
                    ft.Container(
                        content=ft.Text(label, size=16, color=ft.Colors.GREY),
                        width=50,
                        alignment=ft.Alignment(1, 0),
                    ),
                    # 爻线
                    yao_line,
                    # 爻辞和小象传
                    ft.Container(
                        content=ft.Column(
                            [
                                # 爻辞
                                ft.Text(
                                    yao_text,
                                    size=14,
                                    color=text_color,
                                    weight=text_weight,
                                ),
                                # 小象传（如果有）
                                ft.Text(
                                    f"象曰：{xiang_text}" if xiang_text else "",
                                    size=12,
                                    color=text_color,
                                    weight=text_weight,
                                    italic=True,
                                )
                                if xiang_text
                                else ft.Container(),
                            ],
                            spacing=2,
                        ),
                        width=400,
                        padding=ft.Padding(left=15, top=0, right=0, bottom=0),
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
            self.controls.append(row)

    def update_gua(
        self,
        original_gua: Gua,
        changing_positions: Optional[List[int]] = None,
        highlighted_positions: Optional[List[int]] = None,
    ):
        """更新卦象"""
        self.original_gua = original_gua
        self.changing_positions = (
            changing_positions if changing_positions is not None else []
        )
        if highlighted_positions is not None:
            self.highlighted_positions = highlighted_positions

        # 重新计算display_gua
        if self.changing_positions:
            self.display_gua = original_gua.get_changed_gua(self.changing_positions)
        else:
            self.display_gua = original_gua

        self._build()
        self.update()


class GuaRelationsView(ft.Column):
    """卦象关系视图"""

    def __init__(self, gua: Gua, on_gua_select=None):
        self.gua = gua
        self.on_gua_select = on_gua_select

        super().__init__(spacing=20)
        self._build()

    def _build(self):
        """构建关系视图"""
        self.controls = []

        # 标题
        self.controls.append(ft.Text("卦象关系", size=20, weight=ft.FontWeight.BOLD))

        # 创建关系卡片 - 按行排列
        # 第一行：错卦、综卦、反卦
        row1 = ft.Row(
            [
                self._create_relation_card("错卦", self.gua.get_dui_gua(), "阴阳全反"),
                self._create_relation_card("综卦", self.gua.get_zong_gua(), "上下颠倒"),
                self._create_relation_card(
                    "反卦", self.gua.get_fan_gua(), "上下卦互换"
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        )

        # 第二行：上互卦、下互卦
        row2 = ft.Row(
            [
                self._create_relation_card(
                    "上互卦", self.gua.get_shang_hu_gua(), "345爻"
                ),
                self._create_relation_card(
                    "下互卦", self.gua.get_xia_hu_gua(), "234爻"
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        )

        self.controls.append(row1)
        self.controls.append(row2)

    def _create_relation_card(self, name: str, gua: Gua, description: str) -> ft.Card:
        """创建关系卡片"""
        trigram_names = {
            "qian": "天",
            "kun": "地",
            "zhen": "雷",
            "gen": "山",
            "kan": "水",
            "li": "火",
            "xun": "风",
            "dui": "泽",
        }
        upper = trigram_names.get(gua.upper_gua, "")
        lower = trigram_names.get(gua.lower_gua, "")

        def on_click(e):
            if self.on_gua_select:
                self.on_gua_select(gua)

        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(name, size=14, weight=ft.FontWeight.BOLD),
                        ft.Text(f"{gua.name} ({upper}{lower}{gua.name})", size=16),
                        ft.Text(description, size=12, color=ft.Colors.GREY),
                    ],
                    spacing=5,
                ),
                padding=15,
                on_click=on_click,
            ),
            elevation=2,
        )

    def update_gua(self, gua: Gua):
        """更新卦象"""
        self.gua = gua
        self._build()
        self.update()


class YijingApp:
    """周易学习应用"""

    def __init__(self):
        self.original_gua: Gua = ALL_GUAS[0]  # 原始卦（本卦）
        self.changing_yaos: List[int] = []  # 变爻位置列表
        self.highlighted_yaos: List[int] = []  # 高亮爻位置列表
        self.page: Optional[ft.Page] = None

    def main(self, page: ft.Page):
        """主入口"""
        self.page = page
        page.title = "周易学习 - 玩索而得"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 20
        page.window.width = 1200
        page.window.height = 800

        # 全屏模式
        page.window.maximized = True
        page.window.full_screen = True

        # 构建UI
        self._build_ui()

    def _build_ui(self):
        """构建用户界面"""
        # 搜索栏
        self.search_field = ft.TextField(
            label="搜索卦象",
            hint_text="输入卦名或简称（如：水天、需）",
            expand=True,
            on_submit=self._on_search,
        )
        search_button = ft.Button(
            "搜索",
            on_click=self._on_search,
        )

        search_row = ft.Row(
            [self.search_field, search_button],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        # 数字定位搜索框（上卦、下卦、动爻）
        self.upper_field = ft.TextField(
            label="上卦",
            hint_text="1-8",
            width=80,
            text_align=ft.TextAlign.CENTER,
            on_submit=self._on_number_search,
        )
        self.lower_field = ft.TextField(
            label="下卦",
            hint_text="1-8",
            width=80,
            text_align=ft.TextAlign.CENTER,
            on_submit=self._on_number_search,
        )
        self.moving_field = ft.TextField(
            label="动爻",
            hint_text="1-6",
            width=80,
            text_align=ft.TextAlign.CENTER,
            on_submit=self._on_number_search,
        )
        number_search_button = ft.Button(
            "数字定位",
            on_click=self._on_number_search,
        )

        number_search_row = ft.Row(
            [
                ft.Text("数字定位:", size=14, weight=ft.FontWeight.BOLD),
                self.upper_field,
                self.lower_field,
                self.moving_field,
                number_search_button,
                # 数字对照提示
                ft.Text("1乾2兑3离4震5巽6坎7艮8坤", size=11, color=ft.Colors.GREY_600),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        # 搜索结果 - 减小高度
        self.search_results = ft.Column(scroll=ft.ScrollMode.AUTO, height=100)

        # 高亮选择区域 - 用于选择重点突出的爻
        self.highlight_checkboxes = []
        # 高亮选择区域 - 用于选择重点突出的爻
        self.highlight_checkboxes = {}
        highlight_row = ft.Row(
            [
                ft.Text("标红:", size=14, weight=ft.FontWeight.BOLD),
                # 上爻到初爻的复选框
                ft.Checkbox(
                    label="上",
                    value=False,
                    on_change=lambda e: self._on_highlight_change(6, e.control.value),
                ),
                ft.Checkbox(
                    label="五",
                    value=False,
                    on_change=lambda e: self._on_highlight_change(5, e.control.value),
                ),
                ft.Checkbox(
                    label="四",
                    value=False,
                    on_change=lambda e: self._on_highlight_change(4, e.control.value),
                ),
                ft.Checkbox(
                    label="三",
                    value=False,
                    on_change=lambda e: self._on_highlight_change(3, e.control.value),
                ),
                ft.Checkbox(
                    label="二",
                    value=False,
                    on_change=lambda e: self._on_highlight_change(2, e.control.value),
                ),
                ft.Checkbox(
                    label="初",
                    value=False,
                    on_change=lambda e: self._on_highlight_change(1, e.control.value),
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        # 本卦视图（包含卦辞和爻辞，点击爻切换阴阳）
        self.hexagram_view = InteractiveHexagramView(
            original_gua=self.original_gua,
            on_yao_click=self._on_yao_click,
            title="玩索而得 - 点击爻切换阴阳",
            highlighted_positions=self.highlighted_yaos,
        )

        # 卦象关系
        self.relations_view = GuaRelationsView(
            self.original_gua,
            on_gua_select=self._on_gua_select,
        )

        # 卦辞详解（使用display_gua的信息）
        self.gua_info = ft.Column(
            [
                ft.Text("彖曰", size=16, weight=ft.FontWeight.BOLD),
                ft.Text(self.original_gua.tuan, size=14),
                ft.Divider(),
                ft.Text("象曰", size=16, weight=ft.FontWeight.BOLD),
                ft.Text(self.original_gua.xiang, size=14),
            ],
            scroll=ft.ScrollMode.AUTO,
            height=300,
        )

        # 中间主区域：卦象（包含卦辞和爻辞）居中 - 占据更多空间
        center_column = ft.Container(
            content=ft.Column(
                [
                    self.hexagram_view,
                ],
                scroll=ft.ScrollMode.AUTO,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=20,
            alignment=ft.Alignment(0, 0),
        )

        # 左侧：卦辞详解
        left_column = ft.Column(
            [
                ft.Text("卦象详解", size=20, weight=ft.FontWeight.BOLD),
                self.gua_info,
            ],
            expand=1,
            scroll=ft.ScrollMode.AUTO,
        )

        # 右侧：卦象关系
        right_column = ft.Column(
            [
                self.relations_view,
            ],
            expand=1,
            scroll=ft.ScrollMode.AUTO,
        )

        # 主内容区 - 卦象居中，占据更多空间
        # 调整比例：减小左右侧宽度，增大中间区域
        main_content = ft.ResponsiveRow(
            [
                ft.Container(left_column, col={"sm": 12, "md": 3, "lg": 2}),
                ft.Container(center_column, col={"sm": 12, "md": 6, "lg": 8}),
                ft.Container(right_column, col={"sm": 12, "md": 3, "lg": 2}),
            ],
            expand=True,
        )

        # 组装页面 - 搜索框放在最底部
        if self.page is not None:
            self.page.add(
                ft.Column(
                    [
                        ft.Text(
                            "周易学习 - 玩索而得", size=28, weight=ft.FontWeight.BOLD
                        ),
                        ft.Text(
                            "点击爻切换阴阳，探索卦象变化",
                            size=14,
                            color=ft.Colors.GREY,
                        ),
                        ft.Divider(),
                        # 主内容区域占据大部分空间
                        ft.Container(
                            content=main_content,
                            expand=True,
                        ),
                        # 底部搜索区域 - 紧凑布局
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Divider(),
                                    search_row,
                                    self.search_results,
                                    number_search_row,
                                    highlight_row,
                                ],
                                spacing=5,
                            ),
                            padding=ft.Padding(left=0, top=5, right=0, bottom=0),
                        ),
                    ],
                    expand=True,
                    spacing=0,
                )
            )

    def _on_search(self, e):
        """处理搜索"""
        query = self.search_field.value.strip()
        if not query:
            return

        results = search_gua(query)

        # 清空并显示结果
        self.search_results.controls = []

        if not results:
            self.search_results.controls.append(
                ft.Text("未找到匹配的卦象", color=ft.Colors.RED)
            )
        else:
            for gua in results[:5]:  # 最多显示5个结果
                trigram_names = {
                    "qian": "天",
                    "kun": "地",
                    "zhen": "雷",
                    "gen": "山",
                    "kan": "水",
                    "li": "火",
                    "xun": "风",
                    "dui": "泽",
                }
                upper = trigram_names.get(gua.upper_gua, "")
                lower = trigram_names.get(gua.lower_gua, "")

                def make_click_handler(g):
                    return lambda e: self._on_gua_select(g)

                result_item = ft.ListTile(
                    title=ft.Text(f"{gua.name} ({upper}{lower}{gua.name})"),
                    subtitle=ft.Text(gua.chinese_name),
                    on_click=make_click_handler(gua),
                )
                self.search_results.controls.append(result_item)

        self.search_results.update()

    def _on_number_search(self, e):
        """处理数字定位搜索"""
        try:
            upper = int(self.upper_field.value) if self.upper_field.value else 0
            lower = int(self.lower_field.value) if self.lower_field.value else 0
            moving = int(self.moving_field.value) if self.moving_field.value else 0
        except ValueError:
            self.search_results.controls = [
                ft.Text("请输入有效的数字", color=ft.Colors.RED)
            ]
            self.search_results.update()
            return

        # 验证输入范围
        if not (1 <= upper <= 8) or not (1 <= lower <= 8):
            self.search_results.controls = [
                ft.Text("上卦和下卦数字必须在1-8之间", color=ft.Colors.RED)
            ]
            self.search_results.update()
            return

        # 查找卦象
        gua = get_gua_by_numbers(upper, lower)

        if not gua:
            self.search_results.controls = [
                ft.Text("未找到对应的卦象", color=ft.Colors.RED)
            ]
            self.search_results.update()
            return

        # 设置动爻（如果输入了动爻）
        self.changing_yaos = []
        if 1 <= moving <= 6:
            self.changing_yaos = [moving]

        # 清空高亮
        self.highlighted_yaos = []

        # 更新所有视图
        self.original_gua = gua
        self.hexagram_view.update_gua(gua, self.changing_yaos, [])
        self.relations_view.update_gua(gua)
        self._update_gua_info(
            gua.get_changed_gua(self.changing_yaos) if self.changing_yaos else gua
        )

        # 显示结果提示
        trigram_names = {
            "qian": "乾",
            "kun": "坤",
            "zhen": "震",
            "gen": "艮",
            "kan": "坎",
            "li": "离",
            "xun": "巽",
            "dui": "兑",
        }
        upper_name = trigram_names.get(gua.upper_gua, "")
        lower_name = trigram_names.get(gua.lower_gua, "")

        moving_text = f" · 动爻：第{moving}爻" if 1 <= moving <= 6 else ""
        self.search_results.controls = [
            ft.ListTile(
                title=ft.Text(f"{gua.name} ({upper_name}{lower_name}{gua.name})"),
                subtitle=ft.Text(f"数字定位：上卦{upper} · 下卦{lower}{moving_text}"),
                selected=True,
            )
        ]
        self.search_results.update()

    def _on_yao_click(self, yao: Yao):
        """处理爻点击 - 切换变爻状态"""
        if yao.position in self.changing_yaos:
            self.changing_yaos.remove(yao.position)
        else:
            self.changing_yaos.append(yao.position)

        # 更新本卦视图（显示变化后的样子、卦辞、卦名、爻辞）
        self.hexagram_view.update_gua(
            self.original_gua, self.changing_yaos, self.highlighted_yaos
        )

        # 更新卦辞详解
        if self.changing_yaos:
            changed_gua = self.original_gua.get_changed_gua(self.changing_yaos)
            self._update_gua_info(changed_gua)
        else:
            self._update_gua_info(self.original_gua)

    def _update_gua_info(self, gua: Gua):
        """更新卦辞信息"""
        self.gua_info.controls = [
            ft.Text("彖曰", size=16, weight=ft.FontWeight.BOLD),
            ft.Text(gua.tuan, size=14),
            ft.Divider(),
            ft.Text("象曰", size=16, weight=ft.FontWeight.BOLD),
            ft.Text(gua.xiang, size=14),
        ]
        self.gua_info.update()

    def _on_gua_select(self, gua: Gua):
        """处理卦象选择"""
        self.original_gua = gua
        self.changing_yaos = []
        self.highlighted_yaos = []

        # 更新所有视图
        self.hexagram_view.update_gua(gua, [], [])
        self.relations_view.update_gua(gua)

        # 更新卦辞信息
        self._update_gua_info(gua)

        # 清空搜索结果
        self.search_results.controls = []
        self.search_results.update()

    def _on_highlight_change(self, position: int, is_checked: bool):
        """处理高亮选择变化"""
        if is_checked:
            if position not in self.highlighted_yaos:
                self.highlighted_yaos.append(position)
        else:
            if position in self.highlighted_yaos:
                self.highlighted_yaos.remove(position)

        # 更新视图，传递高亮位置
        self.hexagram_view.update_gua(
            self.original_gua, self.changing_yaos, self.highlighted_yaos
        )


def main():
    """程序入口"""
    init_data()
    app = YijingApp()
    ft.run(app.main)


if __name__ == "__main__":
    main()
