package com.asist.asistmod.block;

import java.util.concurrent.atomic.AtomicReference;

import com.asist.asistmod.datamodels.CollapseBlock.RubbleCollapseModel;
import com.asist.asistmod.datamodels.PositionRange.PositionRangeModel;
import com.asist.asistmod.missionhelpers.rubble_collapse.RubbleCollapseManager;
import com.asist.asistmod.missionhelpers.timer.MissionTimer;
import com.asist.asistmod.mqtt.InternalMqttClient;

import net.minecraft.block.Block;
import net.minecraft.block.BlockBasePressurePlate;
import net.minecraft.block.material.Material;
import net.minecraft.block.state.IBlockState;
import net.minecraft.entity.Entity;
import net.minecraft.entity.player.EntityPlayer;
import net.minecraft.init.MobEffects;
import net.minecraft.potion.PotionEffect;
import net.minecraft.server.MinecraftServer;
import net.minecraft.util.math.BlockPos;
import net.minecraft.world.World;
import net.minecraft.world.gen.structure.template.Template.EntityInfo;

public class BlockRubble_Collapse extends Block {
	
	boolean shouldActivate;
	long lastTriggeredTime;

    public PositionRangeModel positionRange = null;
	public String fillBlockType = null;

	protected BlockRubble_Collapse(Material materialIn) {
		super(materialIn);

		shouldActivate = true;
		lastTriggeredTime = 0;

		System.out.println("BlockRubble_Collapse: Constructor");
	}
	
	
    /**
     * Triggered whenever an entity collides with this block (enters into the block)
     */
    @Override
	public void onEntityWalk(World worldIn, BlockPos pos, Entity entityIn)
    {
    	if(!worldIn.isRemote && entityIn instanceof EntityPlayer) {
    		
    		//get this block from rubble collapse manager
    		
    		//System.out.println("Walked over collapse block");
    		
    		PositionRangeModel prm = RubbleCollapseManager.getBlock(pos);
    		
    		long lastTimeTriggered = RubbleCollapseManager.getLastCollapseTime(pos);
    		
    		//System.out.println( " Testing we exist --> " + pos.toString() +" "+ lastTimeTriggered);

			if ( (prm != null) && (lastTimeTriggered != 5000000)) {
				
				long time = MissionTimer.getElapsedMillisecondsGlobal();
				
				if( ( time - lastTimeTriggered) >= InternalMqttClient.modSettings.rubbleCollapseBlockInterval ) {	
					
					RubbleCollapseManager.setCollapseTime(pos, time);
					
					MinecraftServer server = worldIn.getMinecraftServer();	
					
					String cmd = "fill " + prm.getString() +  " ";
					
					String [] replaceBlockTypes = {"minecraft:air","minecraft:dark_oak_door","minecraft:wooden_door","minecraft:spruce_door","minecraft:birch_door"};
					
					for (String block : replaceBlockTypes) {
						
						String fullCommand = "";
						
						if (fillBlockType != null) {
							fullCommand = cmd + fillBlockType + " 0 replace " + block;						
						}
						else {
							fullCommand = cmd + "minecraft:gravel 0 replace " + block;
						}					
						
						server.commandManager.executeCommand(server, fullCommand);
						System.out.println("BlockRubble_Collapse: cmd = " + fullCommand);
					}					

											
					
					String playerName = entityIn.getName();					
					
					String pid = InternalMqttClient.name_to_pid(playerName);
					
					RubbleCollapseModel message = new RubbleCollapseModel(playerName,pid, pos.getX(), pos.getY(),pos.getZ(),prm.from.getX(),
							prm.from.getY(),prm.from.getZ(),prm.to.getX(),prm.to.getY(),prm.to.getZ());	    
	    			
	    			InternalMqttClient.publish(message.toJsonString(), "observations/events/player/rubble_collapse",playerName);
				}
					
			}				
				
		}
    }
}
