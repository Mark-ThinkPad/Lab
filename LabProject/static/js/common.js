$(function () {
    // 自动修改页脚年份
    let year = new Date().getFullYear();
    $('#footer-year').text(year);
    let preset_label = $('#csvFile_label').html();
    $('#csvFile').change(function () {
        try {
            let file = this.files[0];
            $('#csvFile_label').html(file.name);
            if ( !/\.(csv)$/.test(file.name)) {
                alert('选择的文件必须是列名为"content"的csv文件!');
                // 清空文件
                $('#csvFile').val('');
                $('#csvFile_label').html(preset_label);
            }
        } catch (e) {
            $('#csvFile_label').html(preset_label);
        }
    });
});