package com.asist.asistmod.missionhelpers.RoleManager;

import java.util.concurrent.ConcurrentHashMap;

import com.asist.asistmod.missionhelpers.datastructures.Player;
import com.asist.asistmod.missionhelpers.datastructures.PlayerManager;
import com.asist.asistmod.missionhelpers.enums.RoleType;
import com.asist.asistmod.missionhelpers.freezeManager.FreezeManager;
import com.asist.asistmod.missionhelpers.mission.Mission;

import net.minecraft.entity.player.EntityPlayer;
import net.minecraft.init.MobEffects;
import net.minecraft.potion.PotionEffect;

public class RoleManager {
	
	private static final ConcurrentHashMap<String,RoleTypeLight> roleMap = new ConcurrentHashMap<String,RoleTypeLight>();
		
	public static void assignRoleToPlayer(String name, RoleTypeLight role ){
		
		if( roleMap.containsKey(name) ) {			
			roleMap.replace(name, role);		
		}
		else {			
			roleMap.put(name, role);			
		}		
	}
	
	public static RoleTypeLight getPlayerRole(String name) {
		
		if( !roleMap.containsKey(name) ) {			
			 assignRoleToPlayer(name, RoleTypeLight.NULL );
		}
		return roleMap.get(name);
		
	}
	
	public static boolean isPlayerMedic(String name) {
		
		return roleMap.get(name) == RoleTypeLight.MED;
	}
	
	public static boolean isPlayerEng(String name) {
		
		return roleMap.get(name) == RoleTypeLight.ENG;
	}
	
	public static boolean isPlayerTran(String name) {
		
		return roleMap.get(name) == RoleTypeLight.TRAN;
	}
	
	public static void setRoleEffects(EntityPlayer entityPlayer, RoleTypeLight role) {
		
		entityPlayer.clearActivePotions();
		PotionEffect potionEffect = null;
		PotionEffect noJump = new PotionEffect(MobEffects.JUMP_BOOST, 100000, 128, true, false);
		
		Player player = PlayerManager.getPlayer(entityPlayer);

		switch(role) {

			case MED:
				entityPlayer.addPotionEffect(noJump);
				entityPlayer.getFoodStats().setFoodLevel(6);
				if (player.isCarryingVictim) {
					potionEffect = new PotionEffect(MobEffects.SLOWNESS, 100000, 3, true, false);
					entityPlayer.addPotionEffect(potionEffect);
				}
				break;
			case ENG:
				if (player.isCarryingVictim) {
					//SLOWER THAN SLOW
					potionEffect = new PotionEffect(MobEffects.SLOWNESS, 100000, 3, true, false);
				}
				else {
					//SLOW
					potionEffect = new PotionEffect(MobEffects.SLOWNESS, 100000, 1, true, false);
				}
				entityPlayer.addPotionEffect(potionEffect);
				entityPlayer.addPotionEffect(noJump);
				entityPlayer.getFoodStats().setFoodLevel(6);			
				break;
			case TRAN:
				potionEffect = new PotionEffect(MobEffects.SPEED, 100000, 1, true, false);
				entityPlayer.addPotionEffect(potionEffect);
				entityPlayer.addPotionEffect(noJump);
				entityPlayer.getFoodStats().setFoodLevel(6);			
				break;
			default:
				entityPlayer.addPotionEffect(noJump);
				entityPlayer.getFoodStats().setFoodLevel(6);	
				break;
		}
		if (FreezeManager.isPlayerFrozen(entityPlayer.getName())) {
			potionEffect = new PotionEffect(MobEffects.BLINDNESS, 99999, 255, true, false);
			entityPlayer.addPotionEffect(potionEffect);
			potionEffect = new PotionEffect(MobEffects.SLOWNESS, 99999, 10, true, false);
			entityPlayer.addPotionEffect(potionEffect);
		}
	}
	
	public static String printRoleMap() {
		StringBuilder sb = new StringBuilder("");
		
		roleMap.forEach((k,v) -> {
			sb.append(k);
			sb.append( " : ");
			sb.append( v.name() );
			sb.append( "\n" );
		});
		
		return sb.toString();
	}
	

}


