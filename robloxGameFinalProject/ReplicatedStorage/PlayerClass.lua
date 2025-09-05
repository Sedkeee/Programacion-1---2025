local PlayerClass = {}
PlayerClass.__index = PlayerClass

function PlayerClass.new(name, health, speed)
	local self = setmetatable({}, PlayerClass)
	self._name = name or "Default"
	self._health = health or 100
	self._speed = speed or 16
	return self
end

function PlayerClass:GetHealth() return self._health end
function PlayerClass:GetSpeed() return self._speed end
function PlayerClass:GetName() return self._name end

function PlayerClass:ApplyStats(player)
	error("ApplyStats debe implementarse en subclase")
end

return PlayerClass
