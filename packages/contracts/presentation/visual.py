"""Typed block visual settings. No executable or raw renderer options."""
from typing import Annotated, Literal
from pydantic import Field, model_validator
from packages.contracts.semantic import Strict

ChartKind = Literal['line','bar','area','stacked_bar','combo','scatter','bubble','histogram','boxplot','heatmap','calendar_heatmap','pie','donut','treemap','sunburst','tree','waterfall','funnel','sankey','range_timeline','map','map_points','map_routes','radar','graph','chord','parallel','theme_river','candlestick','pictorial_bar','effect_scatter','gauge','progress']
ColorRole = Literal['primary','secondary','violet','green','orange','red','muted']
LabelPosition = Literal['top','bottom','left','right','inside','insideTop','insideBottom']

class VisualSeries(Strict):
    key: str = Field(min_length=1, max_length=120)
    name: str = Field(default='', max_length=200)
    visible: bool = True
    kind: Literal['line','bar','area'] = 'line'
    color: ColorRole = 'primary'
    axis: Literal['auto','left','right'] = 'auto'
    width: Annotated[int, Field(ge=1,le=6)] = 2
    stroke: Literal['solid','dashed','dotted'] = 'solid'
    shape: Literal['straight','smooth','step'] = 'straight'
    points: bool = True
    labels: bool | None = None
    label_position: LabelPosition | None = None
    fill_opacity: Annotated[float, Field(ge=0,le=1)] = .15

class VisualColumn(Strict):
    key: str = Field(min_length=1,max_length=120)
    name: str = Field(default='',max_length=200)
    visible: bool = True
    width: Annotated[int, Field(ge=60,le=600)] = 160
    align: Literal['left','center','right'] = 'right'
    wrap: bool = False
    decimals: Annotated[int, Field(ge=0,le=8)] | None = None
    bars: bool = False

class ConditionalColor(Strict):
    column: str = Field(default='value',max_length=120)
    operator: Literal['gt','lt','eq'] = 'gt'
    value: float
    color: ColorRole = 'green'
    whole_row: bool = False

class BlockVisual(Strict):
    series: list[VisualSeries] = Field(default_factory=list,max_length=30)
    columns: list[VisualColumn] = Field(default_factory=list,max_length=50)
    conditions: list[ConditionalColor] = Field(default_factory=list,max_length=30)
    decimals: Annotated[int, Field(ge=0,le=8)] = 2
    compact: bool = False
    labels: bool = False
    label_position: LabelPosition = 'top'
    label_rotate: Annotated[int, Field(ge=-90,le=90)] = 0
    hide_overlap: bool = True
    horizontal: bool = False
    bar_width: Annotated[int, Field(ge=4,le=100)] = 32
    bar_gap: Annotated[int, Field(ge=0,le=100)] = 20
    legend_position: Literal['top','bottom','left','right'] = 'bottom'
    x_visible: bool = True
    y_visible: bool = True
    x_title: str = Field(default='',max_length=200)
    y_title: str = Field(default='',max_length=200)
    y_right_title: str = Field(default='',max_length=200)
    x_rotate: Literal[0,45,90] = 0
    y_min: float | None = None
    y_max: float | None = None
    grid_lines: bool = True
    tooltip: bool = True
    tooltip_previous: bool = True
    tooltip_comparison: bool = True
    zoom: bool = False
    animation: bool = True
    goal: float | None = None
    goal_label: str = Field(default='',max_length=200)
    gauge_min: float = 0
    gauge_max: float = 100
    pie_radius: Annotated[int, Field(ge=10,le=80)] = 45
    start_angle: Annotated[int, Field(ge=0,le=360)] = 90
    symbol_size: Annotated[int, Field(ge=2,le=60)] = 10
    row_numbers: bool = False
    freeze_header: bool = True
    freeze_first: bool = False
    paginate: bool = False
    page_size: Literal[10,25,50,100] = 25
    text_align: Literal['left','center','right'] = 'left'
    text_size: Literal['small','normal','large'] = 'normal'

    @model_validator(mode="after")
    def consistent_settings(self):
        import math
        for value in (self.y_min, self.y_max, self.goal, self.gauge_min, self.gauge_max):
            if value is not None and not math.isfinite(value):
                raise ValueError("VISUAL_FINITE_NUMBER_REQUIRED")
        if self.y_min is not None and self.y_max is not None and self.y_min >= self.y_max:
            raise ValueError("VISUAL_AXIS_RANGE_INVALID")
        if self.gauge_min >= self.gauge_max:
            raise ValueError("VISUAL_GAUGE_RANGE_INVALID")
        for items in (self.series, self.columns):
            if len({item.key for item in items}) != len(items):
                raise ValueError("VISUAL_DUPLICATE_KEY")
        for condition in self.conditions:
            if not math.isfinite(condition.value):
                raise ValueError("VISUAL_FINITE_NUMBER_REQUIRED")
        return self
