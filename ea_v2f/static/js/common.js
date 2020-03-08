$(document).ready(function () {
    // 自动修改页脚年份
    let year = new Date().getFullYear();
    $('#footer-year').text(year);
});