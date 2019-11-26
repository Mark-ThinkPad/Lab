$(function () {
    // 判空函数
    function isEmpty(input_id, button_id) {
        let input = $(input_id).val();
        if (input !== '') {
            $(button_id).attr('disabled', false);
        } else {
            $(button_id).attr('disabled', true);
        }
    }
    // 自动显示文件名 +　判空
    let preset_label = $('#csvFile_label').html();
    $('#csvFile').change(function () {
        try {
            let file = this.files[0];
            $('#csvFile_label').html(file.name);
            if ( !/\.(csv)$/.test(file.name)) {
                alert('请选择列名为"content"的csv文件!');
                // 清空文件
                $('#csvFile').val('');
                $('#csvFile_label').html(preset_label);
                $('#upload_csvFile').attr('disabled', true);
                return false
            }
            $('#upload_csvFile').attr('disabled', false);
        } catch (e) {
            $('#csvFile_label').html(preset_label);
            $('#upload_csvFile').attr('disabled', true);
        }
    });
    // 输入判空
    $('#words').bind('input propertychange', function () {
        isEmpty('#words', '#upload_words')
    });
    // 回车触发按钮
    $('#words').keydown(function (e) {
        if (e.keyCode === 13) {
            $('#upload_words').click();
        }
    });
    function some_buttons(api_url, data) {
        $.ajax({
            url: api_url,
            type: 'POST',
            data: data,
            dataType: 'json',
            success: function (data) {
                if (data.status === 1) {
                    $('#result').html(data.message);
                } else if (data.status === 0) {
                    alert(data.message);
                    window.location.reload();
                }
            },
            error: function (jpXHR) {
                alert('Status Code: ' + jpXHR.status);
            },
        });
    }
    // 发送ajax请求分析一句话
    $('#upload_words').click(function () {
        // 还是先判空
        let words = $('#words').val();
        if (words !== '') {
            let data = {
                words: words,
                client_id: Cookies.get('client_id'),
            };
            some_buttons('/api/getContent/', data);
        } else {
            $('#upload_words').attr('disabled', true);
            alert('请输入一句话!');
        }
    });
    // 上传csv文件
    $('#upload_csvFile').click(function () {
        let csv = $('#csvFile').val();
        if (csv !== '') {
            $('#result').html('请耐心等待csv写入pandas');
            let form_data = new FormData();
            let f = document.getElementById('csvFile');
            form_data.append('client_id', Cookies.get('client_id'));
            form_data.append('csvFile', f.files[0]);
            $.ajax({
                url: '/api/getFile/',
                type: 'POST',
                data: form_data,
                dateType: 'json',
                cache: false,
                contentType: false,
                processData: false,
                success: function (data) {
                    if (data.status === 1) {
                        $('#result').html(data.message);
                    } else if (data.status === 0) {
                        alert(data.message);
                        window.location.reload();
                    }
                },
                error: function (jpXHR) {
                    alert('Status Code: ' + jpXHR.status);
                },
            });
        } else {
            $('#upload_csvFile').attr('disabled', true);
            alert('请选择列名为"content"的csv文件!')
        }
    });
    // 下面三个按钮
    $('#getCRFModel').click(function () {
        let data = {client_id: Cookies.get('client_id')};
        some_buttons('/api/get/CRFModel/', data);
    });
    $('#getDictModel').click(function () {
        let data = {client_id: Cookies.get('client_id')};
        some_buttons('/api/get/DictModel/', data);
    });
    $('#getAtrain').click(function () {
        let data = {client_id: Cookies.get('client_id')};
        some_buttons('/api/get/Atrain/', data);
    });
});