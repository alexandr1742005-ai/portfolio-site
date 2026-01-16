// Анимация появления карточек
document.addEventListener('DOMContentLoaded', () => {
    const cards = document.querySelectorAll('.smooth-fade, .slide-in');
    
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
    });
});
