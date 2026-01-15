document.addEventListener('DOMContentLoaded', () => {
    // Находим все карточки
    const cards = document.querySelectorAll('.card');

    // Проходимся по каждой карточке
    cards.forEach(card => {
        // Делаем её невидимой и чуть выше
        card.style.opacity = 0;
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.6s, transform 0.6s';

        // Через 300 миллисекунд (0.3 секунды)
        setTimeout(() => {
            // Делаем её видимой и на своём месте
            card.style.opacity = 1;
            card.style.transform = 'translateY(0)';
        }, 300);
    });
});
