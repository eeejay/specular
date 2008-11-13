<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
                xmlns:revtree="http://monotonous.org">

<xsl:template match="/sidebyside">
  <html>
    <head>
      <link rel="stylesheet" type="text/css" href="api-compare.css" />
      <script type="text/javascript" src="api-compare.js" />
      <title><xsl:value-of select="title"/></title>
    </head>
    <body>
      <h1><xsl:value-of select="title"/></h1>
      <table id="compareTable">
        <tr>
          <th><xsl:value-of select="//left/@profile"/></th>
          <th><xsl:value-of select="//right/@profile"/></th>
        </tr>
        <tr>
          <xsl:apply-templates select="left"/> 
          <xsl:apply-templates select="right"/> 
        </tr>
      </table>
      <p id="legend">
		  <span class="revInserted" id="labelInserted">Inserted</span>
	      <xsl:text> </xsl:text>
		  <span class="revDeleted" id="labelDeleted">Deleted</span>
	      <xsl:text> </xsl:text>
		  <span class="revAttribUpdate" id="labelAttribUpdate">Updated</span>
      </p>
    </body>
  </html>
</xsl:template>

<xsl:template match="left|right">
  <td class="compareColumn">
	<xsl:attribute name="onmouseover">
	  <xsl:text>mouseOverTree(this);</xsl:text>
	</xsl:attribute>
	<xsl:attribute name="onmouseout">
	  <xsl:text>mouseOutTree(this);</xsl:text>
	</xsl:attribute>
    <ul class="compareTree">
      <xsl:attribute name="tabindex">0</xsl:attribute>
      <xsl:attribute name="multiselectable">
		<xsl:text>multiselectable</xsl:text>
	  </xsl:attribute>
	  <xsl:attribute name="aria-activedescendant">
		<xsl:value-of select="accessible/@revtree:id"/>
	  </xsl:attribute>
	  <xsl:attribute name="onfocus">
		<xsl:text>onTreeFocus(this);</xsl:text>
	  </xsl:attribute>
	  <xsl:attribute name="onblur">
		<xsl:text>OnTreeBlur(this);</xsl:text>
	  </xsl:attribute>
	  <xsl:attribute name="onkeydown">
		<xsl:text>return nodeKeyCallback(event);</xsl:text>
	  </xsl:attribute>
	  <xsl:attribute name="onkeypress">
		<xsl:text>return nodeKeyCallback(event);</xsl:text>
	  </xsl:attribute>
	  <xsl:attribute name="role">tree</xsl:attribute>
      <xsl:apply-templates/> 
    </ul>
  </td>
</xsl:template>

<xsl:template match="accessible">
  <li role="treeitem">
	<xsl:attribute name="aria-expanded">
	  <xsl:text>false</xsl:text>
	</xsl:attribute>
    <xsl:attribute name="class">
      <xsl:call-template name="itemClass"/>
    </xsl:attribute>
	<xsl:attribute name="id">
	  <xsl:value-of select="@revtree:id"/>
	</xsl:attribute>
    <xsl:attribute name="aria-labelledby">
      <xsl:call-template name="labeledBy"/>
      <xsl:text> </xsl:text>
      <xsl:value-of select="@revtree:id"/>Title</xsl:attribute>
	<div role="presentation">
      <span role="label">
	    <xsl:attribute name="onclick">
		  <xsl:text>onNodeClick(this);</xsl:text>
		</xsl:attribute> 
		<xsl:attribute name="class">
          <xsl:call-template name="nodeTitleClass"/>
		</xsl:attribute>
		<xsl:attribute name="onmouseover">
		  <xsl:text>mouseOverNode(this);</xsl:text>
		</xsl:attribute> 
		<xsl:attribute name="onmouseout">
		  <xsl:text>mouseOutNode(this);</xsl:text>
		</xsl:attribute>
	    <xsl:attribute name="id">
		  <xsl:value-of select="@revtree:id"/>
		  <xsl:text>Title</xsl:text>
		</xsl:attribute>
		<xsl:value-of select="@role"/>
	  </span>
      <xsl:call-template name="detailsTable"/>
      <ul role="group">
        <xsl:if test="count(child::*)">
          <xsl:apply-templates/> 
        </xsl:if>
      </ul>
	</div>
  </li>
</xsl:template>

<xsl:template match="//accessible/@*">
  <xsl:variable name="fieldtitle" 
				select="concat(translate(substring(name(),1,1), 
						'abcdefghijklmnopqrstuvwxyz',
						'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 
						substring(name(),2))"/>
  <tr role="presentation">
	<td class="fieldname">
	  <xsl:attribute name="id">
		<xsl:value-of select="../@revtree:id"/>
		<xsl:value-of select="$fieldtitle"/>
		<xsl:text>Field</xsl:text>
	  </xsl:attribute>
	  <xsl:value-of select="$fieldtitle"/>
	</td>
	<td class="fieldvalue" role="presentation">
	  <span>
		<xsl:attribute name="aria-labelledby">
		  <xsl:value-of select="../@revtree:id"/>
		  <xsl:value-of select="$fieldtitle"/>
		  <xsl:text>Field</xsl:text>
		</xsl:attribute>
		<xsl:variable name="baseclass" 
					  select="concat('accessible', $fieldtitle)"/>
		<xsl:choose>
		  <xsl:when test="contains(../@revtree:updatedAttribs, name())">
			<xsl:attribute name="class">
			  <xsl:value-of select="concat($baseclass,' revUpdated')"/>
			</xsl:attribute> 
		  </xsl:when>
		  
		  <xsl:when test="contains(../@revtree:deletedAttribs, name())">
			<xsl:attribute name="class">
			  <xsl:value-of select="concat($baseclass,' revDeleted')"/>
			</xsl:attribute> 
		  </xsl:when>
		  
		  <xsl:when test="contains(../@revtree:insertedAttribs, name())">
			<xsl:attribute name="class">
			  <xsl:value-of select="concat($baseclass,' revInserted')"/>
			</xsl:attribute> 
		  </xsl:when>
		  
		  <xsl:otherwise>
			<xsl:attribute name="class">
			  <xsl:value-of select="$baseclass"/>
			</xsl:attribute> 
		  </xsl:otherwise>
		  
		</xsl:choose>
		<xsl:value-of select="." />
	  </span>
	</td>
  </tr>
</xsl:template>

<xsl:template name="detailsTable">
  <div class="accDetails walkable hiddenDetails" role="treeitem">
	<xsl:attribute name="aria-hidden">true</xsl:attribute>
	<xsl:attribute name="id">
	  <xsl:value-of select="@revtree:id"/>
	  <xsl:text>Dialog</xsl:text>
	</xsl:attribute>
	<table role="presentation">
	  <tbody role="presentation">
		<xsl:apply-templates select="@name"/>
		<xsl:apply-templates select="@role"/>
		<xsl:apply-templates select="@description"/>
		<xsl:apply-templates select="@state"/>
		<xsl:apply-templates select="@value"/>
		<xsl:apply-templates select="@actions"/>
	  </tbody>
	</table>
  </div>
</xsl:template>
  
<xsl:template name="labeledBy">
  <xsl:choose>
	<xsl:when test="contains(@revtree:changes, 'deleted-self')">
	  <xsl:text>labelDeleted</xsl:text>
	</xsl:when>
	<xsl:when test="contains(@revtree:changes, 'inserted-self')">
	  <xsl:text>labelInserted</xsl:text>
	</xsl:when>
	<xsl:when test="contains(@revtree:changes, 'updated-attrib')">
	  <xsl:text>labelAttribUpdate</xsl:text>
	</xsl:when>
	<xsl:when test="contains(@revtree:changes, 'inserted-attrib')">
	  <xsl:text>labelAttribUpdate</xsl:text>
	</xsl:when>
  </xsl:choose>
</xsl:template>

<xsl:template name="nodeTitleClass">
  nodeTitle
  <xsl:if test="contains(@revtree:changes, 'moved-self')">		
	revMoved
  </xsl:if>
  <xsl:if test="contains(@revtree:changes, 'deleted-self')">
	revDeleted
  </xsl:if>
  <xsl:if test="contains(@revtree:changes, 'inserted-self')">
	revInserted
  </xsl:if>
  <xsl:if test="contains(@revtree:changes, 'updated-attrib')">
	revAttribUpdate
  </xsl:if>
  <xsl:if test="contains(@revtree:changes, 'inserted-attrib')">
	revAttribUpdate
  </xsl:if>
</xsl:template>

<xsl:template name="itemClass">
  <xsl:text>treeNode walkable </xsl:text>
  <xsl:choose>
    <xsl:when test="preceding-sibling::*">
      <xsl:choose>
        <xsl:when test="following-sibling::*">
          middle
        </xsl:when>
        <xsl:otherwise>
          last
        </xsl:otherwise>
      </xsl:choose>
    </xsl:when>
    <xsl:otherwise>
      <xsl:choose>
        <xsl:when test="following-sibling::*">
          first
        </xsl:when>
        <xsl:otherwise>
          single
        </xsl:otherwise>
    </xsl:choose>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

</xsl:stylesheet>
