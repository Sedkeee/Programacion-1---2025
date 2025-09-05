local PlayerClass = require(game:GetService("ReplicatedStorage"):WaitForChild("PlayerClass"))
local ELN = setmetatable({}, {__index = PlayerClass})
ELN.__index = ELN

function ELN.new()
	local self = PlayerClass.new("ELN", 100, 24)
	setmetatable(self, ELN)
	return self
end

local function applyToHumanoid(self, player, char)
	local humanoid = char:WaitForChild("Humanoid", 5)
	if not humanoid then
		warn("[ELN] no humanoid for "..player.Name)
		return
	end

	local function apply()
		humanoid.MaxHealth = self:GetHealth()
		humanoid.Health = self:GetHealth()
		humanoid.WalkSpeed = self:GetSpeed()
		print(string.format("[ELN] %s -> MaxHealth=%d WalkSpeed=%d", player.Name, humanoid.MaxHealth, humanoid.WalkSpeed))
	end

	apply()
	task.delay(0.2, apply)
	task.delay(0.6, apply)
	task.delay(1.2, apply)
end

function ELN:ApplyStats(player)
	local function onChar(char) applyToHumanoid(self, player, char) end
	if player.Character then onChar(player.Character) end
	player.CharacterAdded:Connect(onChar)
end

return ELN
