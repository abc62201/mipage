def 主页默认脚本():
    脚本文本='''
// 全局变量
let currentClassify = null;
let currentRecordId = null;
let allClassifies = [];
let currentContextClassify = null;  // 当前右键点击的分类名

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    bindEvents();
    
    if (window.pywebview && window.pywebview.api) {
        loadClassifies();
    } else {
        window.addEventListener('pywebviewready', function() {
            loadClassifies();
        });
    }
});

// 从后端加载分类列表
async function loadClassifies() {
    try {
        allClassifies = await pywebview.api.获取所有分类();
        renderClassifyList(allClassifies);
    } catch (error) {
        console.error('加载分类失败:', error);
        document.getElementById('classify_list').innerHTML = 
            '<div class="empty_tip">加载失败: ' + error + '</div>';
    }
}

// 渲染分类列表
function renderClassifyList(classifies) {
    const listContainer = document.getElementById('classify_list');
    
    if (!classifies || classifies.length === 0) {
        listContainer.innerHTML = '<div class="empty_tip">暂无分类，请点击上方 + 添加</div>';
        return;
    }
    
    let html = '';
    classifies.forEach(classify => {
        const activeClass = classify === currentClassify ? 'active' : '';
        html += `<div class="classify_item ${activeClass}" data-classify="${classify}">${classify}</div>`;
    });
    listContainer.innerHTML = html;
    
    // 绑定左键点击事件
    document.querySelectorAll('.classify_item').forEach(item => {
        item.addEventListener('click', function() {
            document.querySelectorAll('.classify_item').forEach(el => el.classList.remove('active'));
            this.classList.add('active');
            const classify = this.dataset.classify;
            selectClassify(classify);
        });
        
        // 绑定右键菜单事件
        item.addEventListener('contextmenu', function(e) {
            e.preventDefault();
            e.stopPropagation();
            currentContextClassify = this.dataset.classify;
            const menu = document.getElementById('classify_context_menu');
            menu.style.left = e.pageX + 'px';
            menu.style.top = e.pageY + 'px';
            menu.style.display = 'block';
        });
    });
}

// 选择分类
async function selectClassify(classify) {
    currentClassify = classify;
    document.getElementById('current_classify').textContent = classify;
    document.getElementById('search_input').value = '';
    await loadRecords(classify);
}

// 加载分类下的数据
async function loadRecords(classify, keyword = "") {
    try {
        const records = await pywebview.api.获取分类下的数据(classify, keyword);
        renderRecords(records);
    } catch (error) {
        console.error('加载数据失败:', error);
        document.getElementById('content_grid').innerHTML = 
            '<div class="empty_tip">加载失败: ' + error + '</div>';
    }
}

// 渲染记录卡片
function renderRecords(records) {
    const gridContainer = document.getElementById('content_grid');
    
    if (!records || records.length === 0) {
        gridContainer.innerHTML = '<div class="empty_tip">该分类下暂无数据</div>';
        return;
    }
    
    let html = '';
    records.forEach(record => {
        const imageHtml = record.image 
            ? `<img src="${record.image}" alt="${record.name}" onerror="this.parentElement.innerHTML='<span class=\\'no_image\\'>📷</span>'" />`
            : '<span class="no_image">📷</span>';
        
        html += `
        <div class="card" data-id="${record.id}">
            <div class="card_name" title="${record.name}">${record.name}</div>
            <div class="card_image" data-url="${record.url}">
                ${imageHtml}
            </div>
            <div class="card_info">
                <div class="card_row">
                    <span class="card_label">账号:</span>
                    <span class="card_value" title="${record.username}">${record.username || '-'}</span>
                    <button class="copy_btn" data-copy="${record.username}">复制</button>
                </div>
                <div class="card_row">
                    <span class="card_label">密码:</span>
                    <span class="card_value" title="${record.password}">${record.password || '-'}</span>
                    <button class="copy_btn" data-copy="${record.password}">复制</button>
                </div>
            </div>
        </div>
        `;
    });
    gridContainer.innerHTML = html;
    
    bindCardEvents();
}

// 绑定卡片事件
function bindCardEvents() {
    // 点击图片打开浏览器
    document.querySelectorAll('.card_image').forEach(img => {
        img.addEventListener('click', function(e) {
            e.stopPropagation();
            const url = this.dataset.url;
            if (url) {
                pywebview.api.打开浏览器(url);
            }
        });
    });
    
    // 复制按钮
    document.querySelectorAll('.copy_btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.stopPropagation();
            const text = this.dataset.copy;
            if (text) {
                copyToClipboard(text);
                this.textContent = '已复制';
                setTimeout(() => { this.textContent = '复制'; }, 1000);
            }
        });
    });
    
    // 右键菜单
    document.querySelectorAll('.card').forEach(card => {
        card.addEventListener('contextmenu', function(e) {
            e.preventDefault();
            currentRecordId = this.dataset.id;
            showContextMenu(e.pageX, e.pageY);
        });
    });
}

// 复制到剪贴板
function copyToClipboard(text) {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    document.body.removeChild(textarea);
}

// 显示右键菜单
function showContextMenu(x, y) {
    const menu = document.getElementById('context_menu');
    menu.style.left = x + 'px';
    menu.style.top = y + 'px';
    menu.style.display = 'block';
}

// 隐藏右键菜单
function hideContextMenu() {
    document.getElementById('context_menu').style.display = 'none';
}

// 绑定所有事件
function bindEvents() {
    // 点击页面其他地方隐藏右键菜单
    document.addEventListener('click', hideContextMenu);
    
    // 添加分类按钮
    document.getElementById('add_classify_btn').addEventListener('click', function() {
        document.getElementById('add_modal').style.display = 'flex';
        document.getElementById('new_classify_input').focus();
    });
    
    // 确认添加分类
    document.getElementById('confirm_add_btn').addEventListener('click', async function() {
        const input = document.getElementById('new_classify_input');
        const classifyName = input.value.trim();
        
        if (!classifyName) {
            alert('请输入分类名称');
            return;
        }
        
        try {
            const result = await pywebview.api.添加分类(classifyName);
            if (result.success) {
                document.getElementById('add_modal').style.display = 'none';
                input.value = '';
                loadClassifies();
            } else {
                alert('添加失败: ' + result.message);
            }
        } catch (error) {
            alert('添加失败: ' + error);
        }
        
    });
    
    // 取消添加分类
    document.getElementById('cancel_add_btn').addEventListener('click', function() {
        document.getElementById('add_modal').style.display = 'none';
        document.getElementById('new_classify_input').value = '';
    });
    
    // 回车确认添加分类
    document.getElementById('new_classify_input').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            document.getElementById('confirm_add_btn').click();
        }
    });
    
    // 添加记录按钮
    document.getElementById('add_record_btn').addEventListener('click', function() {
        if (!currentClassify) {
            alert('请先选择一个分类');
            return;
        }
        openRecordModal('添加记录', {
            classify: currentClassify,
            name: '',
            url: '',
            username: '',
            password: '',
            image: '',
            note: ''
        });
    });
    
    // 搜索按钮
    document.getElementById('search_btn').addEventListener('click', function() {
        if (!currentClassify) return;
        const keyword = document.getElementById('search_input').value.trim();
        loadRecords(currentClassify, keyword);
    });
    
    // 搜索回车
    document.getElementById('search_input').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            document.getElementById('search_btn').click();
        }
    });
    
    // 刷新截图按钮
    document.getElementById('refresh_screenshot_btn').addEventListener('click', async function() {
        try {
            const result = await pywebview.api.触发截图任务();
            alert(result.message);
        } catch (error) {
            alert('操作失败: ' + error);
        }
    });
    
    // 导出CSV按钮
    document.getElementById('export_csv_btn').addEventListener('click', function() {
        // 更新当前分类名称显示
        document.getElementById('export_classify_name').textContent = currentClassify || '未选择';
        // 如果没有选择分类，禁用"仅导出当前分类"选项
        const currentRadio = document.querySelector('input[name="export_scope"][value="current"]');
        currentRadio.disabled = !currentClassify;
        currentRadio.parentElement.style.opacity = currentClassify ? '1' : '0.5';
        // 显示弹窗
        document.getElementById('export_modal').style.display = 'flex';
    });
    
    // 确认导出
    document.getElementById('confirm_export_btn').addEventListener('click', async function() {
        const scope = document.querySelector('input[name="export_scope"]:checked').value;
        
        try {
            let result;
            if (scope === 'all') {
                result = await pywebview.api.导出所有密码();
            } else {
                if (!currentClassify) {
                    alert('请先选择一个分类');
                    return;
                }
                result = await pywebview.api.导出当前分类(currentClassify);
            }
            
            if (result.success) {
                document.getElementById('export_modal').style.display = 'none';
                alert(result.message + '\\n\\n文件位置: ' + result.file);
            } else {
                alert('导出失败: ' + result.message);
            }
        } catch (error) {
            alert('导出失败: ' + error);
        }
    });
    
    // 取消导出
    document.getElementById('cancel_export_btn').addEventListener('click', function() {
        document.getElementById('export_modal').style.display = 'none';
    });
    
    // 点击导出弹窗外部关闭
    document.getElementById('export_modal').addEventListener('click', function(e) {
        if (e.target === this) {
            this.style.display = 'none';
        }
    });
    
    
        // ========== 分类右键菜单 ==========

    
    // 点击页面其他地方隐藏分类右键菜单
    document.addEventListener('click', function() {
        document.getElementById('classify_context_menu').style.display = 'none';
    });
    
    // 右键菜单 - 重命名
    document.querySelector('[data-classify-action="rename"]').addEventListener('click', function() {
        document.getElementById('classify_context_menu').style.display = 'none';
        if (!currentContextClassify) return;
        
        document.getElementById('old_classify_name').textContent = currentContextClassify;
        document.getElementById('new_classify_name_input').value = currentContextClassify;
        document.getElementById('rename_modal').style.display = 'flex';
        setTimeout(() => document.getElementById('new_classify_name_input').focus(), 100);
    });
    
    // 右键菜单 - 删除分类
    document.querySelector('[data-classify-action="delete"]').addEventListener('click', async function() {
        document.getElementById('classify_context_menu').style.display = 'none';
        if (!currentContextClassify) return;
        
        // 二次确认
        const confirmed = confirm(`确定要删除分类 "${currentContextClassify}" 吗？\n\n⚠️ 该分类下的所有记录都将被删除，此操作不可恢复！`);
        if (!confirmed) return;
        
        try {
            const result = await pywebview.api.删除分类(currentContextClassify);
            if (result.success) {
                alert(result.message);
                // 如果删除的是当前选中的分类，清空右侧
                if (currentClassify === currentContextClassify) {
                    currentClassify = null;
                    document.getElementById('current_classify').textContent = '请选择分类';
                    document.getElementById('content_grid').innerHTML = '<div class="empty_tip">请从左侧选择一个分类</div>';
                }
                loadClassifies();
            } else {
                alert('删除失败: ' + result.message);
            }
        } catch (error) {
            alert('删除失败: ' + error);
        }
    });
    
    // 确认重命名
    document.getElementById('confirm_rename_btn').addEventListener('click', async function() {
        
        const newName = document.getElementById('new_classify_name_input').value.trim();
        
        if (!newName) {
            alert('请输入新的分类名称');
            return;
        }
        
        if (newName === currentContextClassify) {
            alert('新名称与原名称相同');
            return;
        }
        
        try {
            const result = await pywebview.api.重命名分类(currentContextClassify, newName);
            if (result.success) {
                document.getElementById('rename_modal').style.display = 'none';
                alert(result.message);
                // 如果重命名的是当前选中的分类，更新显示
                if (currentClassify === currentContextClassify) {
                    currentClassify = newName;
                }
                loadClassifies();
                if (currentClassify) {
                    loadRecords(currentClassify);
                }
            } else {
                alert('重命名失败: ' + result.message);
            }
        } catch (error) {
            alert('重命名失败: ' + error);
        }
    });
    
    // 取消重命名
    document.getElementById('cancel_rename_btn').addEventListener('click', function() {
        document.getElementById('rename_modal').style.display = 'none';
    });
    
    // 回车确认重命名
    document.getElementById('new_classify_name_input').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            document.getElementById('confirm_rename_btn').click();
        }
    });
    
    // 点击重命名弹窗外部关闭
    document.getElementById('rename_modal').addEventListener('click', function(e) {
        if (e.target === this) {
            this.style.display = 'none';
        }
    });
    
    
    // 右键菜单 - 修改
    document.querySelector('[data-action="edit"]').addEventListener('click', async function() {
        hideContextMenu();
        const records = await pywebview.api.获取分类下的数据(currentClassify);
        const record = records.find(r => r.id == currentRecordId);
        if (record) {
            openRecordModal('修改记录', record);
        }
    });
    
    // 右键菜单 - 移动
    document.querySelector('[data-action="move"]').addEventListener('click', function() {
        hideContextMenu();
        openMoveModal();
    });
    
    // 右键菜单 - 删除
    document.querySelector('[data-action="delete"]').addEventListener('click', async function() {
        hideContextMenu();
        if (confirm('确定要删除这条记录吗？')) {
            try {
                const result = await pywebview.api.删除密码记录(currentRecordId);
                if (result.success) {
                    loadRecords(currentClassify);
                } else {
                    alert('删除失败: ' + result.message);
                }
            } catch (error) {
                alert('删除失败: ' + error);
            }
        }
    });
    
    // 确认保存记录
    document.getElementById('confirm_record_btn').addEventListener('click', async function() {
        const id = document.getElementById('record_id').value;
        const data = {
            classify: document.getElementById('record_classify').value,
            name: document.getElementById('record_name').value.trim(),
            url: document.getElementById('record_url').value.trim(),
            username: document.getElementById('record_username').value.trim(),
            password: document.getElementById('record_password').value.trim(),
            image: document.getElementById('record_image').value.trim(),
            note: document.getElementById('record_note').value.trim()
        };
        
        if (!data.name) {
            alert('请输入名称');
            return;
        }
        
        try {
            let result;
            if (id) {
                result = await pywebview.api.修改密码记录(id, data.classify, data.name, data.url, data.username, data.password, data.note, data.image);
            } else {
                result = await pywebview.api.添加密码记录(data.classify, data.name, data.url, data.username, data.password, data.note, data.image);
            }
            
            if (result.success) {
                document.getElementById('record_modal').style.display = 'none';
                loadClassifies();
                loadRecords(currentClassify);
            } else {
                alert('保存失败: ' + result.message);
            }
        } catch (error) {
            alert('保存失败: ' + error);
        }
    });
    
    // 取消保存记录
    document.getElementById('cancel_record_btn').addEventListener('click', function() {
        document.getElementById('record_modal').style.display = 'none';
    });
    
    // 确认移动
    document.getElementById('confirm_move_btn').addEventListener('click', async function() {
        const newClassify = document.getElementById('move_classify_select').value;
        if (!newClassify) {
            alert('请选择目标分类');
            return;
        }
        
        try {
            const result = await pywebview.api.移动到其他分类(currentRecordId, newClassify);
            if (result.success) {
                document.getElementById('move_modal').style.display = 'none';
                loadRecords(currentClassify);
            } else {
                alert('移动失败: ' + result.message);
            }
        } catch (error) {
            alert('移动失败: ' + error);
        }
    });
    
    // 取消移动
    document.getElementById('cancel_move_btn').addEventListener('click', function() {
        document.getElementById('move_modal').style.display = 'none';
    });
}

// 打开记录弹窗
function openRecordModal(title, record) {
    document.getElementById('record_modal_title').textContent = title;
    document.getElementById('record_id').value = record.id || '';
    document.getElementById('record_name').value = record.name || '';
    document.getElementById('record_url').value = record.url || '';
    document.getElementById('record_username').value = record.username || '';
    document.getElementById('record_password').value = record.password || '';
    document.getElementById('record_image').value = record.image || '';
    document.getElementById('record_note').value = record.note || '';
    
    const select = document.getElementById('record_classify');
    select.innerHTML = allClassifies.map(c => 
        `<option value="${c}" ${c === record.classify ? 'selected' : ''}>${c}</option>`
    ).join('');
    
    document.getElementById('record_modal').style.display = 'flex';
}

// 打开移动弹窗
function openMoveModal() {
    const select = document.getElementById('move_classify_select');
    select.innerHTML = allClassifies.map(c => 
        `<option value="${c}">${c}</option>`
    ).join('');
    document.getElementById('move_modal').style.display = 'flex';
}
    '''
    return 脚本文本