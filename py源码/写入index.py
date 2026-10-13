def 主页默认文本():
    主页文本='''
<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<meta http-equiv="X-UA-Compatible" content="IE=Edge,chrome=1"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=0.5, maximum-scale=2.0, user-scalable=yes" />
<link rel="stylesheet" href="index.css">
</head>
<body>
<div class="container">
    <!-- 左侧分类菜单 -->
    <div id="left_menu" class="left_menu">
        <div class="menu_header">
            <button id="add_classify_btn" class="add_btn" title="添加分类">+</button>
            <span class="menu_title">分类列表</span>
        </div>
        <div id="classify_list" class="classify_list">
            <div class="loading">正在加载分类...</div>
        </div>
    </div>
    
    <!-- 右侧内容区域 -->
    <div id="right_content" class="right_content">
        <!-- 顶部工具栏 -->
        <div class="content_toolbar">
            <button id="add_record_btn" class="toolbar_btn">+ 添加</button>
            <div class="search_box">
                <input type="text" id="search_input" placeholder="搜索名称..." />
                <button id="search_btn" class="search_btn">🔍</button>
            </div>
            <button id="refresh_screenshot_btn" class="toolbar_btn">📸 刷新截图</button>
            <button id="export_csv_btn" class="toolbar_btn export_btn">📥 导出CSV</button>
            <h2 id="current_classify" class="current_title">请选择分类</h2>
        </div>
        
        <!-- 内容网格 -->
        <div id="content_grid" class="content_grid">
            <div class="empty_tip">请从左侧选择一个分类</div>
        </div>
    </div>
</div>

<!-- 添加分类弹窗 -->
<div id="add_modal" class="modal" style="display:none;">
    <div class="modal_content">
        <h3>添加新分类</h3>
        <input type="text" id="new_classify_input" placeholder="请输入分类名称" />
        <div class="modal_buttons">
            <button id="confirm_add_btn">确定</button>
            <button id="cancel_add_btn">取消</button>
        </div>
    </div>
</div>

<!-- 添加/编辑记录弹窗 -->
<div id="record_modal" class="modal" style="display:none;">
    <div class="modal_content record_modal_content">
        <h3 id="record_modal_title">添加记录</h3>
        <input type="hidden" id="record_id" />
        <div class="form_row">
            <label>分类:</label>
            <select id="record_classify"></select>
        </div>
        <div class="form_row">
            <label>名称:</label>
            <input type="text" id="record_name" placeholder="网站/应用名称" />
        </div>
        <div class="form_row">
            <label>网址:</label>
            <input type="text" id="record_url" placeholder="https://..." />
        </div>
        <div class="form_row">
            <label>用户名:</label>
            <input type="text" id="record_username" placeholder="用户名/邮箱" />
        </div>
        <div class="form_row">
            <label>密码:</label>
            <input type="text" id="record_password" placeholder="密码" />
        </div>
        <div class="form_row">
            <label>图片:</label>
            <input type="text" id="record_image" placeholder="图片URL或路径" />
        </div>
        <div class="form_row">
            <label>备注:</label>
            <textarea id="record_note" placeholder="备注信息"></textarea>
        </div>
        <div class="modal_buttons">
            <button id="confirm_record_btn">保存</button>
            <button id="cancel_record_btn">取消</button>
        </div>
    </div>
</div>

<!-- 右键菜单 -->
<div id="context_menu" class="context_menu" style="display:none;">
    <div class="context_item" data-action="edit">✏️ 修改</div>
    <div class="context_item" data-action="move">📁 移动到...</div>
    <div class="context_item" data-action="delete">🗑️ 删除</div>
</div>

<!-- 移动分类弹窗 -->
<div id="move_modal" class="modal" style="display:none;">
    <div class="modal_content">
        <h3>移动到分类</h3>
        <select id="move_classify_select"></select>
        <div class="modal_buttons">
            <button id="confirm_move_btn">确定</button>
            <button id="cancel_move_btn">取消</button>
        </div>
    </div>
</div>

<!-- 分类右键菜单 -->
<div id="classify_context_menu" class="context_menu" style="display:none;">
    <div class="context_item" data-classify-action="rename">✏️ 重命名</div>
    <div class="context_item" data-classify-action="delete">🗑️ 删除分类</div>
</div>

<!-- 重命名分类弹窗 -->
<div id="rename_modal" class="modal" style="display:none;">
    <div class="modal_content">
        <h3>重命名分类</h3>
        <p style="margin-bottom: 10px; color: #666;">当前名称: <strong id="old_classify_name"></strong></p>
        <input type="text" id="new_classify_name_input" placeholder="请输入新的分类名称" />
        <div class="modal_buttons">
            <button id="confirm_rename_btn">确定</button>
            <button id="cancel_rename_btn">取消</button>
        </div>
    </div>
</div>
<!-- 导出确认弹窗 -->
<div id="export_modal" class="modal" style="display:none;">
    <div class="modal_content">
        <h3>导出CSV</h3>
        <p style="margin-bottom: 15px; color: #666;">请选择导出范围：</p>
        <div style="margin-bottom: 20px;">
            <label style="display: block; margin-bottom: 10px; cursor: pointer;">
                <input type="radio" name="export_scope" value="all" checked /> 
                导出所有密码记录
            </label>
            <label style="display: block; cursor: pointer;">
                <input type="radio" name="export_scope" value="current" /> 
                仅导出当前分类 (<span id="export_classify_name">未选择</span>)
            </label>
        </div>
        <div class="modal_buttons">
            <button id="confirm_export_btn">导出</button>
            <button id="cancel_export_btn">取消</button>
        </div>
    </div>
</div>

<script src="index.js"></script>
</body>
</html>    
    '''
    return 主页文本