local PlayerClass = require(game:GetService("ReplicatedStorage"):WaitForChild("PlayerClass"))
local Tombos = setmetatable({}, {__index = PlayerClass})
Tombos.__index = Tombos

function Tombos.new()
	local self = PlayerClass.new("Tombos", 200, 16)
	setmetatable(self, Tombos)
	return self
end

local function applyToHumanoid(self, player, char)
	local humanoid = char:WaitForChild("Humanoid", 5)
	if not humanoid then
		warn("[Tombos] no humanoid for "..player.Name)
		return
	end

	local function apply()
		humanoid.MaxHealth = self:GetHealth()
		humanoid.Health = self:GetHealth()
		humanoid.WalkSpeed = self:GetSpeed()
		print(string.format("[Tombos] %s -> MaxHealth=%d WalkSpeed=%d", player.Name, humanoid.MaxHealth, humanoid.WalkSpeed))
	end

	apply()
	task.delay(0.2, apply)
	task.delay(0.6, apply)
	task.delay(1.2, apply)
end

function Tombos:ApplyStats(player)
	local function onChar(char) applyToHumanoid(self, player, char) end
	if player.Character then onChar(player.Character) end
	player.CharacterAdded:Connect(onChar)
end

return Tombos
