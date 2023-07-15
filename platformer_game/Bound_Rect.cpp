#include "Bound_Rect.h"

/////////////////////////////////// CONSTRUCTOR AND DESTRUCTOR FUNCTIONS ////////////////////////////////////////////

Boundrect::Boundrect(sf::Sprite& sprite, sf::Vector2f offset, float width, float height) :sprite(sprite)
{
	bound.setPosition(this->sprite.getPosition().x + offset.x, this->sprite.getPosition().y + offset.y);
	bound.setSize(sf::Vector2f(width, height));
	bound.setOutlineThickness(1.0f);
	bound.setOutlineColor(sf::Color::Red);
	bound.setFillColor(sf::Color::Transparent);
	this->offset.x = offset.x;
	this->offset.y = offset.y;
	rectbound.left = bound.getPosition().x;
	rectbound.top = bound.getPosition().y;
	rectbound.width = width;
	rectbound.height = height;
}

Boundrect::~Boundrect()
{

}

/////////////////////////////////// ACCESSOR FUNCTIONS ////////////////////////////////////////////

void Boundrect::move(sf::Vector2f pos)
{
	sprite.move(pos);
}

/////////////////////////////////// UPDATE FUNCTIONS ////////////////////////////////////////////

void Boundrect::update()
{
	bound.setPosition(this->sprite.getPosition().x + offset.x, this->sprite.getPosition().y + offset.y);
	rectbound.left = bound.getPosition().x;
	rectbound.top = bound.getPosition().y;
}

/////////////////////////////////// RENDER FUNCTIONS ////////////////////////////////////////////

void Boundrect::render(sf::RenderTarget* target)
{
		target->draw(this->bound);
}