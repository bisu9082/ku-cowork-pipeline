# FIGURE RULES — Nature급 matplotlib 수치 기준 (변경 금지)

## rcParams 설정
\`\`\`python
import matplotlib
matplotlib.rcParams.update({
    'font.family':        'sans-serif',
    'font.sans-serif':    ['Arial', 'DejaVu Sans'],
    'font.size':          8,
    'axes.titlesize':     9,
    'axes.labelsize':     8,
    'xtick.labelsize':    7,
    'ytick.labelsize':    7,
    'legend.fontsize':    7,
    'axes.spines.top':    False,
    'axes.spines.right':  False,
    'axes.linewidth':     0.8,
    'axes.axisbelow':     True,
    'axes.grid':          True,
    'grid.linewidth':     0.5,
    'grid.alpha':         0.4,
    'legend.frameon':     False,
    'savefig.dpi':        300,
    'savefig.bbox':       'tight',
    'savefig.pad_inches': 0.05,
    'axes.prop_cycle': matplotlib.cycler('color',
        ['#648FFF','#FE6100','#785EF0','#DC267F','#FFB000','#009E73']),
})
\`\`\`

## Figure 크기 기준
- single column: `figsize=(3.5, 2.8)`
- double column: `figsize=(7.2, 2.8)`
- 2행: `figsize=(3.5, 5.2)`
- **`constrained_layout=True` 필수 / `tight_layout()` 금지**

## Bar Chart 규칙
\`\`\`python
# 범례: 반드시 그래프 바깥
ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
fig, ax = plt.subplots(figsize=(4.5, 2.8), constrained_layout=True)

# 막대 위 레이블 함수 (항상 사용)
def add_bar_labels(ax, fmt='.3f', fs=6.5):
    patches = [p for p in ax.patches if p.get_height() > 0]
    if not patches: return
    ym = max(p.get_height() for p in patches)
    for p in patches:
        ax.annotate(f'{p.get_height():{fmt}}',
            xy=(p.get_x() + p.get_width()/2, p.get_height() + ym*0.02),
            ha='center', va='bottom', fontsize=fs,
            fontweight='bold', annotation_clip=False)
    ax.set_ylim(top=ym * 1.15)

# x축 겹침 방지
ax.set_xticklabels(labels, rotation=45, ha='right', fontsize=7)
\`\`\`

## Figure 자기 검토 5항목 (생성 후 필수)
- [ ] DPI 300 저장 확인
- [ ] 상단/오른쪽 테두리 제거
- [ ] 범례 그래프 외부 배치
- [ ] 막대 위 레이블 여유공간 (y_max × 1.15)
- [ ] x축 레이블 겹침 없음
