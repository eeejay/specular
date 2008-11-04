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
      <p>
        <span class="revInserted">Inserted</span><xsl:text> </xsl:text>
        <span class="revDeleted">Deleted</span><xsl:text> </xsl:text>
        <span class="revUpdated">Updated</span><xsl:text> </xsl:text>
        <span class="revMoved">Moved</span><br/>
        <span><b>[</b>name • role<b>]</b></span>
      </p>
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
    </body>
  </html>
</xsl:template>


<xsl:template match="left">
  <td width="%50">
    <ul>
      <xsl:apply-templates/> 
    </ul>
  </td>
</xsl:template>

<xsl:template match="right">
  <td width="%50">
    <ul>
      <xsl:apply-templates/> 
    </ul>
  </td>
</xsl:template>

<xsl:template match="accessible">
  <li>
    <xsl:variable name="baseclass">accessiblenode</xsl:variable>

	<xsl:choose>

	  <xsl:when test="contains(@revtree:changes, 'moved-self')">
		<xsl:attribute name="class">
		  <xsl:value-of select="concat($baseclass,' revMoved')"/>
		</xsl:attribute> 
	  </xsl:when>

	  <xsl:when test="contains(@revtree:changes, 'deleted-self')">
		<xsl:attribute name="class">
		  <xsl:value-of select="concat($baseclass,' revDeleted')"/>
		</xsl:attribute> 
	  </xsl:when>

	  <xsl:when test="contains(@revtree:changes, 'inserted-self')">
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
    <span>
      <xsl:if test="@revtree:id">
	    <xsl:attribute name="id">
	      <xsl:value-of select="@revtree:id"/>
	    </xsl:attribute> 
      </xsl:if>
	  <xsl:attribute name="onmouseover">highlightNode(this);</xsl:attribute> 
	  <xsl:attribute name="onmouseout">unhighlightNode(this);</xsl:attribute> 
	  <xsl:attribute name="onclick">showDetails(this, true);</xsl:attribute> 
      <b>[</b>
      <xsl:apply-templates select="@name">
        <xsl:with-param name="textdisplay">ellipsize</xsl:with-param>
      </xsl:apply-templates>
 •
      <xsl:apply-templates select="@role"/><b>]</b> 
      <table class="accDetails">
        <tr>
          <td>Name:</td>
          <td><xsl:apply-templates select="@name"/></td>
        </tr>
        <tr>
          <td>Role:</td>
          <td><xsl:apply-templates select="@role"/></td>
        </tr>
        <tr>
          <td>Description:</td>
          <td><xsl:apply-templates select="@description"/></td>
        </tr>
        <tr>
          <td>State:</td>
          <td><xsl:apply-templates select="@state"/></td>
        </tr>
      </table>
    </span>
    <xsl:if test="count(child::*)">
      <ul>
        <xsl:apply-templates/> 
      </ul>
    </xsl:if>
  </li>
</xsl:template>

<xsl:template match="//accessible/@*">
  <xsl:param name="textdisplay">no-ellipsize</xsl:param>
  <span>
	<xsl:variable name="baseclass" 
                  select="concat('accessible', name())"/>
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
    <xsl:choose>
      <xsl:when test="$textdisplay = 'no-ellipsize'">
        <xsl:apply-templates select="." mode="no-ellipsize"/>
      </xsl:when>
	  <xsl:otherwise>
        <xsl:apply-templates select="." mode="ellipsize"/>
	  </xsl:otherwise>
    </xsl:choose>
      
  </span>
</xsl:template>

<xsl:template match="//accessible/@*" mode="no-ellipsize">
  <xsl:value-of select="." /> 
</xsl:template>

<xsl:template match="//accessible/@*" mode="ellipsize">
  <xsl:variable name="len" 
                select="string-length(normalize-space(.))" />
  <xsl:choose> 
    <!-- if collapsed headline_text is 15 characters or longer, 
         display the first 15 characters and add an ellipsis -->
    
    <xsl:when test="$len &gt;= 15"> 
      <xsl:value-of select="substring(normalize-space(.),1,15)"/> 
      <xsl:text> ...</xsl:text> 
    </xsl:when>
    
    <!-- if collapsed headline_text is shorter than  
         15 characters, display it unmodified -->
    <xsl:otherwise> 
      <xsl:value-of select="." /> 
    </xsl:otherwise> 
  </xsl:choose>
</xsl:template>

</xsl:stylesheet>
