local Teams = game:GetService("Teams")
local Players = game:GetService("Players")
local Replicated = game:GetService("ReplicatedStorage")

local TombosClass = require(Replicated:WaitForChild("Tombos"))
local ELNClass = require(Replicated:WaitForChild("ELN"))

local elnTeam = Teams:WaitForChild("ELN")
local tombosTeam = Teams:WaitForChild("TOMBOS")

-- Asegurar que Roblox no autoasigne
if elnTeam then elnTeam.AutoAssignable = false end
if tombosTeam then tombosTeam.AutoAssignable = false end

local function contar(excluir)
	local e,t = 0,0
	for _,p in ipairs(Players:GetPlayers()) do
		if p ~= excluir and p.Team then
			if p.Team == elnTeam then e = e + 1
			elseif p.Team == tombosTeam then t = t + 1 end
		end
	end
	return e,t
end

local function asignar(player)
	local e,t = contar(player)
	if e < t then
		player.Team = elnTeam
	elseif t < e then
		player.Team = tombosTeam
	else
		player.Team = (math.random(1,2) == 1) and elnTeam or tombosTeam
	end
	print("[TeamManager] "..player.Name.." -> ".. tostring(player.Team and player.Team.Name or "nil"))
end

Players.PlayerAdded:Connect(function(player)
	print("[TeamManager] PlayerAdded:", player.Name)

	asignar(player)

	-- Forzar respawn para que aparezca en el spawn del equipo
	task.spawn(function()
		task.wait(0.12) -- pequeño delay
		player:LoadCharacter()
	end)

	-- Crear clase según el equipo y aplicar stats
	local classInstance
	if player.Team == elnTeam then
		classInstance = ELNClass.new()
	else
		classInstance = TombosClass.new()
	end

	classInstance:ApplyStats(player)
end)
