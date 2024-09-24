package com.asist.asistmod.missionhelpers.enums;

import net.minecraft.init.Blocks;
import net.minecraft.item.Item;
import net.minecraft.item.ItemStack;
import net.minecraft.util.ResourceLocation;
import net.minecraftforge.fml.common.registry.ForgeRegistries;

public enum ItemType {
	MEDICALKIT				(1, "MEDKIT", 
								new ItemStack(ForgeRegistries.ITEMS.getValue(new ResourceLocation("asistmod", "item_medical_kit"))),
								" asistmod:item_medical_kit 1 0 "
								+ "{CanDestroy:[\"asistmod:block_victim_1\",\"asistmod:block_victim_2\","
								+ "\"asistmod:block_victim_saved_a\",\"asistmod:block_victim_saved_b\",\"asistmod:block_victim_saved_c\","		
								+ "\"asistmod:block_victim_1b\",\"asistmod:block_victim_proximity\" ]}"),
	STRETCHER				(2, "STRETCHER", 
								new ItemStack(ForgeRegistries.ITEMS.getValue(new ResourceLocation("asistmod", "item_stretcher"))),
								" asistmod:item_stretcher 1 0"),
	STRETCHER_OCCUPIED		(3, "STRETCHER_OCCUPIED", 
								new ItemStack(ForgeRegistries.ITEMS.getValue(new ResourceLocation("asistmod", "item_stretcher_occupied"))),
								" asistmod:item_occupied_stretcher 1 0"),
	HAMMER					(4, "HAMMER", 
								new ItemStack(ForgeRegistries.ITEMS.getValue(new ResourceLocation("asistmod", "item_hammer"))),
								" asistmod:item_hammer 1 0 {CanDestroy:[\"minecraft:gravel\"]}"),
	NULL					(0, "NULL", new ItemStack(Blocks.AIR), " minecraft:air")
	;
	
	private final int code;
	private final String name;
	private final ItemStack item;
	private final String commandText;
	
	ItemType(int code, String name, ItemStack item, String commandText) {
		this.code = code;
		this.name = name;
		this.item = item;
		this.commandText = commandText;
	}
	
	public int getCode() {
		return this.code;
	}
	
	public String getName() {
		return this.name;
	}
	
	public ItemStack getItemStack() {
		return this.item;
	}
	
	public Item getItem() {
		return this.item.getItem();
	}
	
	public String getCommandText() {
		return this.commandText;
	}
	
	public boolean notNull() {
		return !this.name.equals("null");
	}
}
