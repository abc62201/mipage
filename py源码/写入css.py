def 主页默认样式():
    样式文本='''
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html, body {
    height: 100%;
    overflow: hidden;
}

body {
    font-family: "Microsoft YaHei", Arial, sans-serif;
    background: #f5f5f5;
}

.container {
    display: flex;
    height: 100vh;
    width: 100vw;
    overflow: hidden;
}

/* 左侧菜单样式 */
.left_menu {
    width: 250px;
    min-width: 250px;
    background: #2c3e50;
    color: #ecf0f1;
    display: flex;
    flex-direction: column;
    box-shadow: 2px 0 5px rgba(0,0,0,0.1);
    height: 100vh;
}

.menu_header {
    padding: 15px;
    background: #1a252f;
    display: flex;
    align-items: center;
    gap: 10px;
    flex-shrink: 0;
}

.menu_title {
    font-size: 16px;
    font-weight: bold;
}

.add_btn {
    width: 32px;
    height: 32px;
    border: none;
    background: #27ae60;
    color: white;
    font-size: 20px;
    border-radius: 4px;
    cursor: pointer;
    transition: background 0.3s;
}

.add_btn:hover {
    background: #229954;
}

.classify_list {
    flex: 1;
    overflow-y: auto;
    padding: 10px 0;
    min-height: 0;
}

.classify_item {
    padding: 12px 20px;
    cursor: pointer;
    transition: background 0.2s;
    border-left: 3px solid transparent;
}

.classify_item:hover {
    background: #34495e;
}

.classify_item.active {
    background: #34495e;
    border-left-color: #3498db;
}

.loading, .empty_tip {
    text-align: center;
    padding: 20px;
    color: #95a5a6;
}

/* 右侧内容区域样式 */
.right_content {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    height: 100vh;
    min-width: 0;
}

/* 顶部工具栏 */
.content_toolbar {
    padding: 15px 20px;
    background: white;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    display: flex;
    align-items: center;
    gap: 15px;
    flex-shrink: 0;
}

.toolbar_btn {
    padding: 8px 16px;
    border: none;
    background: #3498db;
    color: white;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    white-space: nowrap;
}

.toolbar_btn:hover {
    background: #2980b9;
}

.search_box {
    display: flex;
    gap: 5px;
}

.search_box input {
    padding: 8px 12px;
    border: 1px solid #ddd;
    border-radius: 4px;
    width: 200px;
    font-size: 14px;
}

.search_btn {
    padding: 8px 12px;
    border: none;
    background: #95a5a6;
    color: white;
    border-radius: 4px;
    cursor: pointer;
}

.search_btn:hover {
    background: #7f8c8d;
}

.current_title {
    margin-left: auto;
    color: #2c3e50;
    font-size: 18px;
    white-space: nowrap;
}

/* 内容网格 - 关键修复 */
.content_grid {
    flex: 1;
    padding: 20px;
    overflow-y: auto;
    overflow-x: hidden;
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    grid-auto-rows: min-content;
    gap: 20px;
    align-content: start;
    min-height: 0;
}

/* 卡片样式 - 固定高度布局 */
.card {
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    overflow: hidden;
    transition: transform 0.2s, box-shadow 0.2s;
    cursor: pointer;
    display: flex;
    flex-direction: column;
    width: 100%;
    min-height: 280px;
}

.card:hover {
    transform: translateY(-3px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.card_name {
    padding: 12px;
    background: #34495e;
    color: white;
    font-size: 14px;
    font-weight: bold;
    text-align: center;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    flex-shrink: 0;
}

.card_image {
    width: 100%;
    height: 140px;
    min-height: 140px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #ecf0f1;
    overflow: hidden;
    flex-shrink: 0;
}

.card_image img {
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
}

.card_image .no_image {
    color: #95a5a6;
    font-size: 40px;
}

.card_info {
    padding: 12px;
    flex: 1;
    display: flex;
    flex-direction: column;
}

.card_row {
    display: flex;
    align-items: center;
    padding: 8px 0;
    font-size: 13px;
    border-bottom: 1px solid #f0f0f0;
}

.card_row:last-child {
    border-bottom: none;
}

.card_label {
    color: #7f8c8d;
    width: 50px;
    flex-shrink: 0;
}

.card_value {
    flex: 1;
    color: #2c3e50;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    min-width: 0;
}

.copy_btn {
    padding: 4px 10px;
    border: none;
    background: #3498db;
    color: white;
    border-radius: 3px;
    cursor: pointer;
    font-size: 12px;
    margin-left: 8px;
    flex-shrink: 0;
}

.copy_btn:hover {
    background: #2980b9;
}

/* 弹窗样式 */
.modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}

.modal_content {
    background: white;
    padding: 30px;
    border-radius: 8px;
    min-width: 300px;
    max-height: 90vh;
    overflow-y: auto;
}

.record_modal_content {
    min-width: 400px;
}

.modal_content h3 {
    margin-bottom: 20px;
    color: #2c3e50;
}

.modal_content input,
.modal_content select,
.modal_content textarea {
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 14px;
    margin-bottom: 15px;
}

.modal_content textarea {
    height: 80px;
    resize: vertical;
}

.form_row {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
}

.form_row label {
    width: 60px;
    color: #7f8c8d;
    font-size: 14px;
    flex-shrink: 0;
}

.form_row input,
.form_row select,
.form_row textarea {
    flex: 1;
    margin-bottom: 0;
    min-width: 0;
}

.modal_buttons {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
    margin-top: 20px;
}

.modal_buttons button {
    padding: 8px 20px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
}

#confirm_add_btn,
#confirm_record_btn,
#confirm_move_btn {
    background: #3498db;
    color: white;
}

#confirm_add_btn:hover,
#confirm_record_btn:hover,
#confirm_move_btn:hover {
    background: #2980b9;
}

#cancel_add_btn,
#cancel_record_btn,
#cancel_move_btn {
    background: #95a5a6;
    color: white;
}

#cancel_add_btn:hover,
#cancel_record_btn:hover,
#cancel_move_btn:hover {
    background: #7f8c8d;
}

/* 右键菜单 */
.context_menu {
    position: fixed;
    background: white;
    border-radius: 4px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    z-index: 2000;
    min-width: 120px;
}

.context_item {
    padding: 10px 15px;
    cursor: pointer;
    font-size: 14px;
    transition: background 0.2s;
}

.context_item:hover {
    background: #f0f0f0;
}

.context_item:first-child {
    border-radius: 4px 4px 0 0;
}

.context_item:last-child {
    border-radius: 0 0 4px 4px;
}

/* 滚动条美化 */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 4px;
}

::-webkit-scrollbar-thumb {
    background: #c1c1c1;
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: #a8a8a8;
}
/* 导出按钮样式 */
.export_btn {
    background: #27ae60;
}

.export_btn:hover {
    background: #229954;
}
    '''
    return 样式文本