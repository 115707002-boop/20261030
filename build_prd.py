from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.section import WD_SECTION
from docx.enum.style import WD_STYLE_TYPE
from datetime import date

OUT = r'C:\Users\ncucc\Desktop\20261030\個人行程與任務管理系統_PRD.docx'

def set_cell_shading(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd'); shd.set(qn('w:fill'), fill); tcPr.append(shd)
def set_cell_border(cell, **kwargs):
    tc = cell._tc; tcPr = tc.get_or_add_tcPr(); borders = tcPr.first_child_found_in('w:tcBorders')
    if borders is None: borders = OxmlElement('w:tcBorders'); tcPr.append(borders)
    for edge in ('top','left','bottom','right','insideH','insideV'):
        if edge in kwargs:
            tag='w:'+edge; element=borders.find(qn(tag))
            if element is None: element=OxmlElement(tag); borders.append(element)
            for key,val in kwargs[edge].items(): element.set(qn('w:'+key), str(val))
def set_cell_margins(cell, top=110, start=130, bottom=110, end=130):
    tc = cell._tc; tcPr = tc.get_or_add_tcPr(); mar=tcPr.first_child_found_in('w:tcMar')
    if mar is None: mar=OxmlElement('w:tcMar'); tcPr.append(mar)
    for m,v in [('top',top),('start',start),('bottom',bottom),('end',end)]:
        node=mar.find(qn('w:'+m))
        if node is None: node=OxmlElement('w:'+m); mar.append(node)
        node.set(qn('w:w'),str(v)); node.set(qn('w:type'),'dxa')
def set_repeat_table_header(row):
    trPr=row._tr.get_or_add_trPr(); tblHeader=OxmlElement('w:tblHeader'); tblHeader.set(qn('w:val'),'true'); trPr.append(tblHeader)
def set_font(run, name='Microsoft JhengHei', size=10, bold=None, color='202821'):
    run.font.name=name; run._element.get_or_add_rPr().rFonts.set(qn('w:eastAsia'), name); run._element.get_or_add_rPr().rFonts.set(qn('w:ascii'), name); run._element.get_or_add_rPr().rFonts.set(qn('w:hAnsi'), name)
    run.font.size=Pt(size); run.font.color.rgb=RGBColor.from_string(color)
    if bold is not None: run.bold=bold

def set_p(p, before=0, after=5, line=1.15, keep=False):
    pf=p.paragraph_format; pf.space_before=Pt(before); pf.space_after=Pt(after); pf.line_spacing=line
    if keep: pf.keep_with_next=True

def add_para(doc, text='', style=None, boldlead=None):
    p=doc.add_paragraph(style=style)
    if boldlead and text.startswith(boldlead):
        r=p.add_run(boldlead); set_font(r,bold=True)
        r=p.add_run(text[len(boldlead):]); set_font(r)
    else:
        r=p.add_run(text); set_font(r)
    set_p(p)
    return p

def add_bullet(doc, text, level=0):
    p=doc.add_paragraph(style='List Bullet' if level==0 else 'List Bullet 2')
    r=p.add_run(text); set_font(r,size=9.5)
    set_p(p,after=3,line=1.12)
    return p

def add_number(doc,text):
    p=doc.add_paragraph(style='List Number'); r=p.add_run(text); set_font(r,size=9.5); set_p(p,after=4,line=1.12); return p

def add_table(doc, headers, rows, widths=None):
    t=doc.add_table(rows=1, cols=len(headers)); t.alignment=WD_TABLE_ALIGNMENT.CENTER; t.autofit=False
    if widths:
        for col,w in zip(t.columns,widths): col.width=Inches(w)
    for i,h in enumerate(headers):
        c=t.rows[0].cells[i]; set_cell_shading(c,'315F4B'); c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER; set_cell_margins(c)
        p=c.paragraphs[0]; set_p(p,after=0,line=1.05); r=p.add_run(h); set_font(r,size=9,bold=True,color='FFFFFF')
    set_repeat_table_header(t.rows[0])
    border={'val':'single','sz':'5','color':'D9DED8'}
    for row_idx,row in enumerate(rows):
        cells=t.add_row().cells
        if widths:
            for i,w in enumerate(widths): cells[i].width=Inches(w)
        for i,val in enumerate(row):
            c=cells[i]; c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER; set_cell_margins(c)
            if row_idx%2==1: set_cell_shading(c,'F5F7F4')
            p=c.paragraphs[0]; set_p(p,after=0,line=1.08); r=p.add_run(str(val)); set_font(r,size=8.8)
        for c in cells:
            for edge in ('top','left','bottom','right','insideH','insideV'): set_cell_border(c, **{edge:border})
    for c in t.rows[0].cells:
        for edge in ('top','left','bottom','right','insideH','insideV'): set_cell_border(c, **{edge:border})
    doc.add_paragraph().paragraph_format.space_after=Pt(2)
    return t

doc=Document(); sec=doc.sections[0]; sec.top_margin=Inches(.68); sec.bottom_margin=Inches(.65); sec.left_margin=Inches(.78); sec.right_margin=Inches(.78)
styles=doc.styles
normal=styles['Normal']; normal.font.name='Microsoft JhengHei'; normal._element.rPr.rFonts.set(qn('w:eastAsia'),'Microsoft JhengHei'); normal.font.size=Pt(10); normal.font.color.rgb=RGBColor(32,40,33)
normal.paragraph_format.space_after=Pt(5); normal.paragraph_format.line_spacing=1.15
for style_name,size in [('Title',26),('Heading 1',17),('Heading 2',12),('Heading 3',10.5)]:
    st=styles[style_name]; st.font.name='Microsoft JhengHei'; st._element.rPr.rFonts.set(qn('w:eastAsia'),'Microsoft JhengHei'); st.font.size=Pt(size); st.font.bold=True; st.font.color.rgb=RGBColor(0,0,0); st.paragraph_format.space_before=Pt(14 if style_name!='Title' else 0); st.paragraph_format.space_after=Pt(6); st.paragraph_format.keep_with_next=True
# list font defaults
for sn in ['List Bullet','List Bullet 2','List Number']:
    st=styles[sn]; st.font.name='Microsoft JhengHei'; st._element.rPr.rFonts.set(qn('w:eastAsia'),'Microsoft JhengHei'); st.font.size=Pt(9.5)

p=doc.add_paragraph(style='Title'); r=p.add_run('個人行程與任務管理系統'); set_font(r,size=25,bold=True,color='000000'); set_p(p,after=3,line=1.0)
p=doc.add_paragraph(); r=p.add_run('產品需求文件 PRD'); set_font(r,size=13,bold=True,color='315F4B'); set_p(p,after=12)
p=doc.add_paragraph(); r=p.add_run('版本 1.0　｜　日期 2026 年 10 月 30 日　｜　狀態 初步需求基線'); set_font(r,size=9,color='788278'); set_p(p,after=13)
add_para(doc,'本文件整理目前訪談確認的第一版產品方向：為個人使用者提供每日行程與彈性待辦的單一檢視，並依重要性與精確截止時間推薦任務順序。第一版以瀏覽器前端原型驗證日常安排流程，不含帳號、雲端同步或實際通知服務。')

add_para(doc,'文件資訊','Heading 1')
add_table(doc,['欄位','內容'],[
('產品名稱','日序 Daymark（原型名稱，可於後續確認）'),('產品類型','個人行程與任務管理 Web 前端原型'),('主要使用者','個人使用者；目前以單一使用者場景設計'),('核心目標','協助使用者每天判斷優先順序並管理固定行程與彈性待辦'),('文件依據','依目前需求訪談與已完成的互動原型整理；未確認事項以待決議標示')],[1.45,5.85])

add_para(doc,'1. 產品背景與問題','Heading 1')
add_para(doc,'使用者需要同時掌握有明確開始時間的固定行程，以及可以彈性安排的待辦事項。當兩者分散或待辦只依建立先後排列時，使用者不容易快速判斷當天應先做什麼，也容易忽略重要且即將到期的事項。')
add_para(doc,'產品應把「今日安排」作為主要入口，將待辦與行程放在同一個工作脈絡中，提供可理解的推薦排序，並讓使用者保有手動決策權。')

add_para(doc,'2. 產品目標與成功指標','Heading 1')
add_table(doc,['目標','第一版判定方式'],[
('快速看懂今天','首頁可辨識今日未完成任務、固定行程與完成進度。'),('降低排序負擔','未完成任務依重要性與截止時間產生推薦順序，並指出建議先做項目。'),('便於記錄安排','可新增待辦及固定行程，並可標記任務完成或刪除。'),('維持簡單易用','建立任務不要求填寫預估工時；重要性使用高／中／低三階。')],[1.5,5.8])
add_para(doc,'建議後續以可用性測試驗證：使用者能否在短時間內找出下一個應做事項、能否正確理解排序理由，以及新增一筆任務或行程是否順暢。量化目標與埋點尚待產品驗證後設定。')

add_para(doc,'3. 目標使用者與主要情境','Heading 1')
add_para(doc,'目標使用者為希望管理個人日常安排、需要在多項待辦間判斷先後順序的個人使用者。第一版不處理多人協作、共享行事曆或團隊權限。')
add_table(doc,['情境','使用者需求','預期結果'],[
('開始一天','快速知道今天有哪些安排','看到今日待辦、固定行程與完成進度'),('新增工作','記下任務、重要性與截止時刻','任務即時加入清單並重新排序'),('安排約定','記錄日期、開始與結束時間、地點','行程出現在指定日期的行程區'),('完成任務','標示某項待辦已完成','清單、統計與完成進度同步更新'),('重新判斷','檢視推薦次序並自行調整檢視方式','能切換推薦排序與非推薦檢視')],[1.15,2.65,3.5])

add_para(doc,'4. 範圍與版本界線','Heading 1')
add_para(doc,'第一版包含的功能','Heading 2')
for x in ['今日總覽首頁：展示今日未完成待辦、今日固定行程、任務數量及完成進度。','彈性待辦：名稱、備註、日期、精確截止時間、重要性（高／中／低）、完成狀態。','固定行程：名稱、備註、日期、開始時間、結束時間、選填地點。','推薦排序：根據重要性及截止時間計算建議順序，標示首要推薦項目。','任務操作：新增、完成／重新開啟、刪除；可切換推薦排序與建立順序。','本機資料保存：使用瀏覽器 localStorage 保存項目。','響應式介面：支援桌面及手機寬度的基本操作。'] : add_bullet(doc,x)
add_para(doc,'第一版不包含','Heading 2')
for x in ['登入、帳號管理、多裝置同步、多人共享或權限管理。','與 Google Calendar、Apple Calendar、Outlook 等外部服務整合。','推播、電子郵件、簡訊或背景提醒；目前提醒圖示僅為原型提示。','週／月完整日曆格、重複事件、子任務、附件、標籤與專案管理。','預估工時、時間區塊排程、行程衝突自動偵測。','正式上線所需的後端、備份、資安與資料匯出機制。'] : add_bullet(doc,x)

add_para(doc,'5. 功能需求','Heading 1')
add_table(doc,['編號','需求','驗收條件'],[
('FR-01','查看今日總覽','首頁顯示今日日期、待辦數、今日行程數、今日完成比例；無資料時呈現友善空狀態。'),
('FR-02','建立待辦','使用者可輸入名稱、日期、截止時間、重要性及選填備註後儲存；必填欄位不完整時不得提交。'),
('FR-03','建立固定行程','使用者可輸入名稱、日期、開始時間、結束時間及選填備註／地點後儲存。'),
('FR-04','推薦待辦順序','預設依重要性與截止時間排序；清單首項標示「建議先做」，並呈現簡短推薦說明。'),
('FR-05','完成待辦','點選完成控制項後更新完成狀態、統計與進度；已完成項目可重新開啟。'),
('FR-06','刪除項目','使用者可刪除待辦；刪除前需確認，取消確認時資料維持不變。'),
('FR-07','檢視所有任務','可從側邊導覽查看所有未完成待辦；今日總覽只顯示今日待辦。'),
('FR-08','本機保存','重新載入頁面後仍保留已建立及更新的項目；資料範圍限目前瀏覽器。'),
('FR-09','適配手機','窄螢幕仍能讀取主要資訊、開啟導覽及完成新增流程。')],[.65,1.4,5.25])

add_para(doc,'6. 排序規則與產品建議','Heading 1')
add_para(doc,'已確認的排序依據為重要性與精確截止時間；任務重要性分為高、中、低，不要求使用者填寫預估工時。原型使用簡單加權分數產生建議排序，並依剩餘時間增加緊急程度。這是可供試用的初步規則，不應被視為已定稿的產品政策。')
add_table(doc,['排序原則','原型行為','後續建議'],[
('重要性','高、中、低各自映射不同權重。','保留權重可調整，經使用者測試後確認是否合理。'),
('截止時間','越接近截止時刻，緊急程度分數越高；已逾期項目提高急迫分數。','明確定義已逾期任務是否置頂，以及逾期多日後的處理方式。'),
('並列處理','分數相同時依現有順序／建立順序作穩定排序。','可考慮讓使用者拖曳調整，並提供「恢復建議排序」。'),
('排序說明','首頁顯示首項建議及簡短原因。','建議為每項提供可理解的理由，例如「重要且今天到期」。')],[1.15,3.0,3.15])
add_para(doc,'排序解釋應透明且可預期。實際導入前需與使用者確認「高重要但截止較遠」和「低重要但即將到期」兩者的取捨政策。')

add_para(doc,'7. 資料欄位與驗證','Heading 1')
add_table(doc,['資料類型','欄位','規則'],[
('共用','id、type、name、note、date、created','名稱必填且最多 60 字；備註選填且最多 180 字；日期必填。'),
('待辦','priority、deadline、done','priority 僅接受 high／medium／low；截止時間必填且精確至分鐘；done 為布林值。'),
('固定行程','time、end、location','開始與結束時間必填；地點選填；建議在後續版本驗證結束時間晚於開始時間。')],[1.1,2.2,4.0])
add_para(doc,'資料保存目前採單一瀏覽器 localStorage。清除瀏覽器資料、使用無痕模式或更換裝置可能導致資料無法取得；若要正式長期使用，需另行決定雲端同步、帳號與備份策略。')

add_para(doc,'8. 主要操作流程','Heading 1')
add_para(doc,'新增待辦：今日總覽 → 新增項目 → 選擇彈性待辦 → 填寫名稱、重要性、日期與截止時間 → 儲存 → 系統更新清單和推薦順序。')
add_para(doc,'新增行程：今日總覽 → 新增行程（或新增項目後選擇固定行程）→ 填寫名稱、日期、開始與結束時間 → 選填地點及備註 → 儲存 → 行程依開始時間排序顯示。')
add_para(doc,'完成待辦：點擊任務勾選控制項 → 更新完成狀態 → 同步更新待辦數與今日完成進度。')

add_para(doc,'9. 介面與體驗原則','Heading 1')
for x in ['以「今日」為預設首頁，讓使用者一進入系統即可判斷下一步。','清楚區分固定時間行程與彈性待辦，但維持一致的視覺語言。','優先呈現任務名稱、重要性、截止日期時間及推薦標記；備註作為次要資訊。','使用高／中／低文字標籤搭配色彩，不以顏色作為唯一辨識線索。','新增表單依類型顯示必要欄位，避免行程表單出現無關的任務優先欄位。','提供空狀態、儲存回饋、刪除確認與鍵盤 Escape 關閉對話框等基本互動。'] : add_bullet(doc,x)

add_para(doc,'10. 非功能需求','Heading 1')
add_table(doc,['面向','第一版要求'],[
('可用性','主要新增、完成、檢視流程不依賴外部服務；操作回饋明確。'),('相容性','以現代桌面與行動瀏覽器為目標；精確支援矩陣待確認。'),('效能','一般個人規模資料下，操作後清單應即時更新；不設定未驗證的硬性 SLA。'),('隱私','原型資料留在目前瀏覽器本機；介面需說明無雲端同步。'),('無障礙','按鈕具可理解標籤，表單欄位有標籤，色彩之外另提供文字資訊；完整 WCAG 驗證不在此原型範圍。')],[1.25,6.05])

add_para(doc,'11. 已知限制與待決議事項','Heading 1')
add_table(doc,['議題','目前狀態／建議決議'],[
('截止時間語意','已確認需精確到時分；尚未確認日期在過去時、逾期任務及跨日截止的處理方式。'),
('推薦規則權重','目前原型採簡單權重；需用實際任務案例確認重要性與急迫性的相對影響。'),
('行程與任務的日期範圍','原型含今日總覽及所有任務清單；完整日期瀏覽／週月視圖尚待確認。'),
('重複行程與提醒','尚未納入；需確認是否為高頻情境後再排入後續版本。'),
('資料備份與同步','第一版只有本機保存；若跨裝置使用是必要需求，應列為正式產品前置決策。'),
('排序手動調整','目前切換建立順序，不含拖曳；需確認使用者是否期待永久手動排序。')],[1.55,5.75])

add_para(doc,'12. 版本規劃建議','Heading 1')
add_table(doc,['階段','建議內容','目的'],[
('原型驗證','測試每日總覽、排序理解、新增與完成任務流程。','確認核心價值與資訊架構。'),
('MVP','依測試結果完善日期瀏覽、逾期規則、提醒偏好及資料匯出／備份方案。','支援穩定個人日常使用。'),
('後續探索','評估雲端同步、重複行程、外部行事曆整合及進階排程。','依實際使用頻率與需求排序投入。')],[1.25,3.55,2.5])

add_para(doc,'附錄 原型對應','Heading 1')
add_para(doc,'目前互動原型檔案為 index.html，提供示範資料、桌面／手機版介面、新增待辦與行程、完成／刪除項目、推薦排序及瀏覽器本機保存。原型中的提醒按鈕僅呈現提示，不代表已實作通知服務。正式需求及商業規則仍以後續決議更新本 PRD 為準。')

# Footer with page numbering
for section in doc.sections:
    footer=section.footer
    p=footer.paragraphs[0]; p.alignment=WD_ALIGN_PARAGRAPH.RIGHT
    r=p.add_run('日序 Daymark　·　產品需求文件　　'); set_font(r,size=8,color='7C857C')
    fld=OxmlElement('w:fldSimple'); fld.set(qn('w:instr'),'PAGE'); p._p.append(fld)

doc.core_properties.title='個人行程與任務管理系統 產品需求文件'
doc.core_properties.subject='個人行程與每日優先任務管理系統 PRD'
doc.core_properties.author=''
doc.core_properties.keywords='PRD, 個人行程, 任務管理'
doc.save(OUT)
print(OUT)
