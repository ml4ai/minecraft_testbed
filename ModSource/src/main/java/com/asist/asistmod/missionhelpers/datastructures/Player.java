package com.asist.asistmod.missionhelpers.datastructures;

import com.asist.asistmod.datamodels.TrialInfo.CallSigns;
import com.asist.asistmod.missionhelpers.enums.BlockType;
import com.asist.asistmod.missionhelpers.enums.ItemType;
import com.asist.asistmod.missionhelpers.enums.RoleType;
import com.asist.asistmod.missionhelpers.mapblock.MapBlockManager;
import com.asist.asistmod.missionhelpers.mod.ModRoles;
import com.asist.asistmod.mqtt.InternalMqttClient;

import net.minecraft.entity.player.EntityPlayer;
import net.minecraft.init.MobEffects;
import net.minecraft.potion.Potion;
import net.minecraft.potion.PotionEffect;
import net.minecraft.server.MinecraftServer;
import net.minecraft.util.math.BlockPos;

public class Player {

	private EntityPlayer player;
	private int playerNumber;
	private String playerName;
	private RoleType playerRole;
	private int taskNumber;
	public boolean isCarryingVictim;
	private BlockPos carriedVictimPos;
	private int carriedVictimId;
	public BlockType carriedVictimType;
	public String callSign = null;
	

	
	public Player(EntityPlayer player, int playerNumber) {
		
		this.player = player;
		this.playerNumber = playerNumber;
		playerName = player.getName();
		taskNumber = 0;
		playerRole = RoleType.NULL;
		isCarryingVictim = false;
		carriedVictimId = -1;
		carriedVictimPos = null;
		assignCallSign();
		System.out.println("CallSign for " + playerName + " : " + callSign);
		
		
		//updateRole(player);
	}
	
	public Player(EntityPlayer player) {
		this.player = player;
		playerNumber = 0;
		playerName = player.getName();
		taskNumber = 0;
		playerRole = RoleType.NULL;
		assignCallSign();
		
		System.out.println("CallSign for " + playerName + " : " + callSign);
		//updateRole(player);
	}
	
	public EntityPlayer getEntityPlayer() {
		return player;
	}
	
	public int getCarriedVictimId() {
		return this.carriedVictimId;
	}
	
	public int getPlayerNumber() {
		return playerNumber;
	}
	
	public int getTaskNumber() {
		return taskNumber;
	}
	
	public void taskComplete(MinecraftServer server) {				
		taskNumber++;
	}
	
	public String getName() {
		return playerName;
	}
	public RoleType getRole() {
		return playerRole;
	}
	
	public void teleport(Position pos, MinecraftServer server) {
		String tpCommand = "tp " + player.getName() + " " + pos.getString();
		server.commandManager.executeCommand(server, tpCommand);
		System.out.println(tpCommand);
	}
	
	public void updateRole(RoleType role) {
		playerRole = role;
	}
	
	public void giveEffect(Potion effect) {
		player.clearActivePotions();
		PotionEffect potionEffect = new PotionEffect(effect, 100000, 1, true, false);
		//PotionEffect noJump = new PotionEffect(MobEffects.JUMP_BOOST, 100000, 128, true, false);
		player.addPotionEffect(potionEffect);
		//this.player.addPotionEffect(noJump);
		player.getFoodStats().setFoodLevel(6);	
	}
	
	public void giveEffect(RoleType role) {
		player.clearActivePotions();
		PotionEffect potionEffect = null;
		//PotionEffect noJump = new PotionEffect(MobEffects.JUMP_BOOST, 100000, 128, true, false);

		switch(role) {
			case ADMIN:
				potionEffect = new PotionEffect(MobEffects.SPEED, 100000, 3, true, false);
				player.addPotionEffect(potionEffect);
				break;
			case MED:
				//this.player.addPotionEffect(noJump);
				player.getFoodStats().setFoodLevel(6);			
				break;
			case ENG:
				potionEffect = new PotionEffect(MobEffects.SLOWNESS, 100000, 1, true, false);
				player.addPotionEffect(potionEffect);
				//this.player.addPotionEffect(noJump);
				player.getFoodStats().setFoodLevel(6);			
				break;
			case TRAN:
				potionEffect = new PotionEffect(MobEffects.SPEED, 100000, 1, true, false);
				player.addPotionEffect(potionEffect);
				//this.player.addPotionEffect(noJump);
				player.getFoodStats().setFoodLevel(6);			
				break;
			default:
				//this.player.addPotionEffect(noJump);
				player.getFoodStats().setFoodLevel(6);	
				break;
		}
	}
	
	public void removeEffects() {
		player.clearActivePotions();
		//PotionEffect noJump = new PotionEffect(MobEffects.JUMP_BOOST, 100000, 128, true, false);
		//this.player.addPotionEffect(noJump);
		player.getFoodStats().setFoodLevel(6);	
	}
	
	public void clearInventory() {
		player.inventory.clear();
	}
	
	public void giveItem(String item, MinecraftServer server) {
		this.player.inventory.clear();
		String command = "/replaceitem entity " + playerName + " slot.hotbar.0" + item;
		server.commandManager.executeCommand(server, command);
	}
	
	public void giveItems(String[] items, MinecraftServer server) {
		//this.player.inventory.clear();
		int slotNum = 0;
		for(String item:items) {
			String command = "/replaceitem entity " + playerName + " slot.hotbar." + slotNum + item;
			server.commandManager.executeCommand(server, command);
			slotNum++;
		}
	}
	
	public final String canDestroyMarkers = "{CanDestroy:["
            
            + "\"asistmod:block_marker_red_abrasion\",\"asistmod:block_marker_red_bonedamage\",\"asistmod:block_marker_red_novictim\",\"asistmod:block_marker_red_sos\","
			+ "\"asistmod:block_marker_red_critical\",\"asistmod:block_marker_red_criticalvictim\",\"asistmod:block_marker_red_regularvictim\","		
			+ "\"asistmod:block_marker_red_threat\",\"asistmod:block_marker_red_rubble\",\"asistmod:block_marker_red_wildcard\","
            
            + "\"asistmod:block_marker_green_abrasion\",\"asistmod:block_marker_green_bonedamage\",\"asistmod:block_marker_green_novictim\",\"asistmod:block_marker_green_sos\","
			+ "\"asistmod:block_marker_green_critical\",\"asistmod:block_marker_green_criticalvictim\",\"asistmod:block_marker_green_regularvictim\","		
			+ "\"asistmod:block_marker_green_threat\",\"asistmod:block_marker_green_rubble\",\"asistmod:block_marker_green_wildcard\","

            + "\"asistmod:block_marker_blue_abrasion\",\"asistmod:block_marker_blue_bonedamage\",\"asistmod:block_marker_blue_novictim\",\"asistmod:block_marker_blue_sos\","
			+ "\"asistmod:block_marker_blue_critical\",\"asistmod:block_marker_blue_criticalvictim\",\"asistmod:block_marker_blue_regularvictim\","		
			+ "\"asistmod:block_marker_blue_threat\",\"asistmod:block_marker_blue_rubble\",\"asistmod:block_marker_blue_wildcard\","
            
            + "]}";
	
	public String markerItemString(String type) {
		
		return " asistmod:item_marker_"+ type  +" 1 0 " + canDestroyMarkers;
	}
	
	public void giveRoleTools(MinecraftServer server) {
		String[] items = {};
		if (playerRole == RoleType.ADMIN) {
			items = new String[] {
					" minecraft:nether_star 1 0 {display:{Name:\"Start Mission 1\"}}",
					" minecraft:nether_star 1 0 {display:{Name:\"Start Mission 2\"}}",
					" minecraft:nether_star 1 0 {display:{Name:\"End Mission\"}}"};
		}
		else {
			if(callSign != null) {
				if(InternalMqttClient.modSettings.markerBlocksActive) {						
					if(callSign.contentEquals("Red")) {
						System.out.println("Giving Red markers");
						items = new String[] {
								playerRole.getTool().getCommandText(),
								markerItemString("red_abrasion"),
								markerItemString("red_bonedamage"),
								markerItemString("red_novictim"),
								markerItemString("red_criticalvictim"),
								markerItemString("red_regularvictim"),
								markerItemString("red_threat"),
								markerItemString("red_rubble"),
								markerItemString("red_sos")
						};					
					}
					else if (callSign.contentEquals("Green")) {
						System.out.println("Giving Green markers");
						items = new String[] {
								playerRole.getTool().getCommandText(),
								markerItemString("green_abrasion"),
								markerItemString("green_bonedamage"),
								markerItemString("green_novictim"),
								markerItemString("green_criticalvictim"),
								markerItemString("green_regularvictim"),
								markerItemString("green_threat"),
								markerItemString("green_rubble"),
								markerItemString("green_sos")
						};	
					}
					else if (callSign.contentEquals("Blue")) {
						System.out.println("Giving Blue markers");
						items = new String[] {							
								playerRole.getTool().getCommandText(),
								markerItemString("blue_abrasion"),
								markerItemString("blue_bonedamage"),
								markerItemString("blue_novictim"),
								markerItemString("blue_criticalvictim"),
								markerItemString("blue_regularvictim"),
								markerItemString("blue_threat"),
								markerItemString("blue_rubble"),
								markerItemString("blue_sos")
						};	
					}
					
				}
			}
			else {
				
				System.out.println(" ----------------------------------------------------------------------------------------------------------------------- ");
        		System.out.println(" ----------------------------------------------------------------------------------------------------------------------- ");
        		System.out.println(" Looks like this player's callsign is still null, did the mod call out to Malmo Control for the Trial Info ? ");
        		System.out.println(" ----------------------------------------------------------------------------------------------------------------------- ");
        		System.out.println(" ----------------------------------------------------------------------------------------------------------------------- ");
				
        		items = new String[] {						
						this.playerRole.getTool().getCommandText()
				};
			}			
		}
		giveItems(items, server);
	}
	
	public void giveArmor(MinecraftServer server) {
		
		int color = 0;
		
		if(callSign.contentEquals("Red")) {
			color = 11546150;
		}
		else if (callSign.contentEquals("Green")){
			color = 6192150;
		}
		else if (callSign.contentEquals("Blue")){
			color = 3949738;
		}
		//11546150, ItemType.MEDICALKIT),
		//SS		(2, "search", 6192150, ItemType.STRETCHER),
		//HS		(3, "hammer", 3949738, ItemType.HAMMER),
		//int color = this.playerRole.getColor();
		String[] armors = new String[] 
				{	" slot.armor.head minecraft:leather_helmet 1 0 {display:{color:" + color + "}}",
					" slot.armor.chest minecraft:leather_chestplate 1 0 {display:{color:" + color + "}}",
					" slot.armor.legs minecraft:leather_leggings 1 0 {display:{color:" + color + "}}",
					" slot.armor.feet minecraft:leather_boots 1 0 {display:{color:" + color + "}}" };
		
		for(String armor:armors) {
			String command = "/replaceitem entity " + this.playerName + armor;
			server.commandManager.executeCommand(server, command);
		}
	}
	
	public int carryVictim(BlockPos pos,BlockType type) {
		
		int id  = MapBlockManager.getVictimId(pos);
		isCarryingVictim = true;
		carriedVictimId = id;
		carriedVictimPos = pos;
		carriedVictimType = type;
		MapBlockManager.victimIdMap.remove(pos);
		
		//System.out.println( printVictimState() );
		
		return id;
	}
	
	public void placeVictim(BlockPos newPos) {		
		
		try {		
		
			// REASSIGN ID TO NEW BLOCKPOS
			MapBlockManager.victimIdMap.put(newPos,this.carriedVictimId);		
			
			// RESET VICTIM INFO
			isCarryingVictim = false;
			carriedVictimId = -1;
			carriedVictimPos = null;
			carriedVictimType = null;
			
			//System.out.println(printVictimState(newPos));
			
		}catch(Exception e) {
			e.printStackTrace();
		}
		
	}
	
	public String assignCallSign() {
		
		if (callSign == null){

			callSign = InternalMqttClient.name_to_callsign(playerName);						
		}		
		
		return callSign;
	}
	
	public String printVictimState() {
		
		StringBuilder sb = new StringBuilder();
		
		sb.append("--------- PLAYER CLASS VICTIM STATE :"+ this.playerName +" ---------"+"\n");
		sb.append("isCarryingVictim : " + isCarryingVictim +"\n");
		sb.append("carriedVictimId : " +  carriedVictimId+"\n");
		sb.append("carriedVictimPos : " + (( carriedVictimPos != null) ? carriedVictimPos.toString():"null")+"\n");
		sb.append("carriedVictimType :" + (( carriedVictimType != null) ? carriedVictimType:"null")+"\n");		
		return sb.toString();
	}
	
	public String printVictimState(BlockPos newPos) {
		
		StringBuilder sb = new StringBuilder();
		
		sb.append("--------- PLAYER CLASS VICTIM STATE :"+ this.playerName +" ---------"+"\n");
		sb.append("isCarryingVictim : " + isCarryingVictim+"\n");;
		sb.append("carriedVictimId : " +  carriedVictimId+"\n");
		sb.append("carriedVictimPos : " + (( carriedVictimPos != null) ? carriedVictimPos.toString():"null")+"\n");
		sb.append("carriedVictimType :" + (( carriedVictimType != null) ? carriedVictimType:"null")+"\n");		
		sb.append("--------- ID FROM VICTIM ID MAP : "+MapBlockManager.victimIdMap.get(newPos)+" ---------"+"\n");
		
		return sb.toString();
	}

}
