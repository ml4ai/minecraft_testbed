package com.asist.asistmod.missionhelpers.mod;

import com.asist.asistmod.missionhelpers.enums.ItemType;

import net.minecraft.item.ItemStack;

public class ModItems {

	static ItemType[] tools = { 	ItemType.MEDICALKIT,
									ItemType.STRETCHER,
									ItemType.STRETCHER_OCCUPIED,
									ItemType.HAMMER 
									};
	
	public static ItemType getEnum(ItemStack item) {
		for(ItemType type : ItemType.values()) {
			if(item.getItem() == type.getItem()) { return type; }
		}
		return ItemType.NULL;
	}
	
	public static boolean isItem(ItemStack item, ItemType modItem) {
		return item.getItem() == modItem.getItem();
	}
	
	public static boolean isTool(ItemType item) {
		for(ItemType tool : tools) {
			if(item.equals(tool)) { return true; }
		}
		return false;
	}
}
