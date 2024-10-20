document.addEventListener('DOMContentLoaded', function () {
    const currentUrl = window.location.href;

    // Проверяем, если пользователь на странице авторизации, выделяем кнопку "Войти"
    if (currentUrl.includes('/login/')) {
        document.querySelector('.u-nav-item a[href="{% url 'login' %}"]').classList.add('active');
    }
});